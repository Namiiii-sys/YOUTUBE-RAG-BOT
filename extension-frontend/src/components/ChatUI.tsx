import { useState, useEffect } from "react"
import { onAuthStateChanged, type User } from "firebase/auth"
import { auth } from "../firebase"
import Chatinterface from "./Chatinterface"
import Login from "./Login"

const ChatWrapper = () => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
      setLoading(false)
    })
    return () => unsubscribe()
  }, [])

  if (loading) {
    return (
      <div className="w-[500px] h-[500px] bg-gray-100 flex items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    )
  }

  return (
    <div className="w-[500px] h-[500px] bg-gray-100 text-gray-900 rounded-2xl shadow-md flex flex-col overflow-hidden">
      {!user ? (
        <Login />
      ) : (
        <div className="flex flex-col h-full">
          <div className="flex-1 overflow-hidden">
            <Chatinterface user={user} />
          </div>
        </div>
      )}
    </div>
  )
}

export default ChatWrapper
