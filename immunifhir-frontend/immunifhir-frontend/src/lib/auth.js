import { supabase } from './supabase'

export const getCurrentUser = async () => {
  const { data: { user } } = await supabase.auth.getUser()
  return user
}

// Get JWT token
export const getAuthToken = async () => {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token || null
}

export const logout = async () => {
  await supabase.auth.signOut()
}

// Check if user is logged in
export const isAuthenticated = async () => {
  const user = await getCurrentUser()
  return !!user
}