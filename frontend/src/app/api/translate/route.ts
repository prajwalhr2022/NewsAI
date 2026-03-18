import { NextRequest, NextResponse } from 'next/server'

const LANGUAGE_NAMES: Record<string, string> = {
  hi: 'Hindi',
  kn: 'Kannada',
}

export async function POST(req: NextRequest) {
  try {
    const { articleId, title, summary, targetLang, currentTranslations } = await req.json()

    if (!articleId || !title || !targetLang || targetLang === 'en') {
      return NextResponse.json({ error: 'Invalid params' }, { status: 400 })
    }

    // Return cached translation if already in Supabase
    if (currentTranslations?.[targetLang]) {
      return NextResponse.json({ translation: currentTranslations[targetLang] })
    }

    const langName = LANGUAGE_NAMES[targetLang] ?? targetLang
    const apiKey = process.env.GEMINI_API_KEY
    if (!apiKey) return NextResponse.json({ error: 'No API key' }, { status: 500 })

    const prompt = `Translate the following news title and summary into ${langName}.\nReturn ONLY a JSON object with no markdown:\n{"title": "...", "summary": "..."}\n\nTITLE: ${title}\nSUMMARY: ${summary ?? ''}`

    // Call Gemini via REST directly — no SDK dependency
    const geminiRes = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.1, maxOutputTokens: 500 },
        }),
      }
    )

    if (!geminiRes.ok) {
      const err = await geminiRes.json()
      console.error('Gemini error:', err)
      return NextResponse.json({ error: 'Gemini failed' }, { status: 500 })
    }

    const geminiData = await geminiRes.json()
    const raw = geminiData?.candidates?.[0]?.content?.parts?.[0]?.text ?? '{}'
    const clean = raw.replace(/```json|```/g, '').trim()
    const translation = JSON.parse(clean)

    // Cache to Supabase asynchronously (fire and forget)
    if (articleId && translation.title) {
      const { createClient } = await import('@supabase/supabase-js')
      const sb = createClient(
        process.env.NEXT_PUBLIC_SUPABASE_URL!,
        process.env.SUPABASE_SERVICE_ROLE_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
      )
      const updated = { ...(currentTranslations ?? {}), [targetLang]: translation }
      sb.from('articles').update({ translations: updated }).eq('id', articleId).then(() => {})
    }

    return NextResponse.json({ translation })
  } catch (err) {
    console.error('translate error:', err)
    return NextResponse.json({ error: 'Translation failed' }, { status: 500 })
  }
}
