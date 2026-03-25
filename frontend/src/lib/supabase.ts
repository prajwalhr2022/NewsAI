import { createClient } from '@supabase/supabase-js'

export interface Article {
  id: string
  title: string
  summary: string | null
  source_url: string
  source_name: string | null
  image_url: string | null
  category: string | null
  subcategory: string | null
  is_india_focused: boolean
  language: string
  trend_score: number
  verification_status: 'confirmed' | 'flagged' | 'unverified'
  source_count: number
  published_at: string | null
  fetched_at: string
  tags: string[]
  related_sources: { name: string; url: string; tier: number }[]
  translations: Record<string, { title: string; summary: string }>
}

export interface Category {
  id: string
  name: string
  slug: string
  parent_slug: string | null
  article_count: number
}

export interface TrendingTopic {
  id: string
  topic: string
  score: number
  article_count: number
}

export interface PredictionItem {
  direction: 'up' | 'down' | 'sideways'
  reason: string
  confidence: 'high' | 'medium' | 'low'
}

export interface Predictions {
  id: string
  gold: PredictionItem
  silver: PredictionItem
  oil: PredictionItem
  global_stocks: PredictionItem
  india_stocks: PredictionItem
  generated_at: string
}

export interface ArticleFilters {
  category?: string
  isIndia?: boolean
  search?: string
  limit?: number
  offset?: number
  orderBy?: 'fetched_at' | 'trend_score'
}

const supabaseUrl  = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnon)

export async function getArticles(filters: ArticleFilters = {}): Promise<Article[]> {
  const { category, isIndia, search, limit = 100, offset = 0, orderBy = 'fetched_at' } = filters

  let query = supabase
    .from('articles')
    .select('*')
    .order(orderBy, { ascending: false })
    .range(offset, offset + limit - 1)

  if (category && category !== 'all') {
    query = query.eq('category', category)
  }
  if (isIndia !== undefined) {
    query = query.eq('is_india_focused', isIndia)
  }
  if (search && search.trim()) {
    query = query.ilike('title', `%${search.trim()}%`)
  }

  const { data, error } = await query
  if (error) { console.error('getArticles error:', error); return [] }
  return (data as Article[]) ?? []
}

export async function getTopArticles(filters: ArticleFilters = {}): Promise<Article[]> {
  const { category, isIndia, limit = 8 } = filters

  let query = supabase
    .from('articles')
    .select('*')
    .gte('source_count', 2)
    .order('trend_score', { ascending: false })
    .limit(limit)

  if (category && category !== 'all') query = query.eq('category', category)
  if (isIndia !== undefined) query = query.eq('is_india_focused', isIndia)

  const { data, error } = await query
  if (error) { console.error('getTopArticles error:', error); return [] }
  return (data as Article[]) ?? []
}

export async function getCategories(): Promise<Category[]> {
  const { data, error } = await supabase
    .from('categories')
    .select('*')
    .gte('article_count', 2)
    .is('parent_slug', null)
    .order('article_count', { ascending: false })

  if (error) { console.error('getCategories error:', error); return [] }
  return (data as Category[]) ?? []
}

export async function getTrendingTopics(): Promise<TrendingTopic[]> {
  const { data, error } = await supabase
    .from('trending_topics')
    .select('*')
    .order('score', { ascending: false })
    .limit(10)

  if (error) { console.error('getTrendingTopics error:', error); return [] }
  return (data as TrendingTopic[]) ?? []
}

export async function getPredictions(): Promise<Predictions | null> {
  const { data, error } = await supabase
    .from('predictions')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(1)
    .single()

  if (error) return null
  return data as Predictions
}
