import { NextRequest, NextResponse } from 'next/server'
import { GoogleGenAI } from '@google/genai'
import { supabase } from '@/lib/supabase'

const genai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! })

const LANGUAGE_NAMES: Record<string, string> = {
  hi: 'Hindi', ta: 'Tamil', te: 'Telugu',
  ml: 'Malayalam', bn: 'Bengali', mr: 'Marathi', kn: 'Kannada',
}

export async function POST(req: NextRequest) {
  try {
    const { articleId, title, summary, targetLang, currentTranslations } = await req.json()

    if (!articleId || !title || !targetLang || targetLang === 'en') {
      return NextResponse.json({ error: 'Invalid params' }, { status: 400 })
    }

    // Return cached translation if available
    if (currentTranslations?.[targetLang]) {
      return NextResponse.json({ translation: currentTranslations[targetLang] })
    }

    const langName = LANGUAGE_NAMES[targetLang] ?? targetLang
    const prompt = (
      `Translate the following news title and summary into ${langName}.\n` +
      `Return ONLY a JSON object (no markdown): {"title": "...", "summary": "..."}\n\n` +
      `TITLE: ${title}\nSUMMARY: ${summary ?? ''}`
    )

    const response = await genai.models.generateContent({
      model: 'gemini-2.0-flash',
      contents: prompt,
    })

    const raw = response.text?.replace(/```json|```/g, '').trim() ?? '{}'
    const translation = JSON.parse(raw)

    // Cache to Supabase asynchronously
    const updated = { ...(currentTranslations ?? {}), [targetLang]: translation }
    supabase.from('articles').update({ translations: updated }).eq('id', articleId).then(() => {})

    return NextResponse.json({ translation })
  } catch (err) {
    console.error('translate error:', err)
    return NextResponse.json({ error: 'Translation failed' }, { status: 500 })
  }
}