"use client"
import { useState, useRef, useEffect } from "react"
import { BsFillSendFill } from "react-icons/bs"
import { FiLogOut } from "react-icons/fi"
import ReactMarkdown from "react-markdown"
import { type User, signOut } from "firebase/auth"
import { auth } from "../firebase"

type ChatMessage = {
  type: "user" | "bot";
  text: string;
};

type ChatProps = {
  user: User
}

const Chatinterface = ({ user }: ChatProps) => {
  const [chat, setchat] = useState<ChatMessage[]>([])
  const [loading, setloading] = useState(false)
  const [question, setquestion] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chat, loading])

  const getCurrentTabUrl = (): Promise<string> => {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ type: "GET_CURRENT_TAB_URL" }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error getting URL:", chrome.runtime.lastError)
        } else {
          console.log("Fetched URL from background:", response.url)
        }
        resolve(response?.url || "")
      })
    })
  }

  const handleLogout = async () => {
    try {
      await signOut(auth)
    } catch (error) {
      console.error("Error signing out:", error)
    }
  }

  const handleAsk = async () => {
    if (!question.trim()) return

    const currentQuestion = question
    setquestion("") // Clear input immediately
    setloading(true)
    setchat(prev => [...prev, { type: "user", text: currentQuestion }])

    try {
      const VideoUrl = await getCurrentTabUrl()
      if (!VideoUrl || !VideoUrl.includes("youtube.com/watch")) {
        setchat(prev => [...prev, { type: "bot", text: "Please open a YouTube video page to chat!" }])
        setloading(false)
        return
      }

      const token = await user.getIdToken()

      const res = await fetch(
        `http://127.0.0.1:8000/query?video_url=${encodeURIComponent(VideoUrl)}&question=${encodeURIComponent(currentQuestion)}`,
        {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        }
      )

      if (!res.ok) {
        const text = await res.text()
        console.error("API Error:", res.status, text)
        throw new Error(`Server returned ${res.status}: ${text.slice(0, 100)}`)
      }

      const data = await res.json()
      setchat(prev => [...prev, { type: "bot", text: data.answer || "No message detected" }])
    } catch (err: any) {
      console.error("Error while fetching:", err)
      setchat(prev => [...prev, { type: "bot", text: `Error: ${err.message || "Unknown error"}` }])
    }

    setloading(false)
  }

  return (
    <div className="w-full h-full px-6 py-5 overflow-hidden bg-gray-100 rounded-xl shadow-md flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-800">YouTube Assistant</h1>
        <button
          onClick={handleLogout}
          className="text-gray-500 hover:text-red-500 transition-colors p-2 rounded-full hover:bg-gray-200"
          title="Sign out"
        >
          <FiLogOut size={20} />
        </button>
      </div>

      <div className="flex-1 w-full border border-indigo-950 rounded-lg p-3 overflow-y-auto space-y-2">
        {chat.map((msg, i) => (
          <div
            key={i}
            className={`p-2 break-words whitespace-pre-wrap rounded-2xl text-sm w-fit max-w-[75%] ${msg.type === "user" ? "bg-black ml-auto text-white" : "bg-gray-300 text-black"}`}
          >
            {msg.type === "user" ? (
              <p>{msg.text}</p>
            ) : (
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            )}
          </div>
        ))}
        {loading && <div className="text-sm text-gray-500">Loading...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="mt-4 flex justify-between gap-2 rounded-xl border border-indigo-950 w-full">
        <input
          type="text"
          placeholder="Ask your query..."
          value={question}
          onChange={(e) => setquestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          className="focus:outline-none w-full p-2 rounded-xl"
        />
        <button onClick={handleAsk}>
          <BsFillSendFill className="w-10 h-10 p-2" />
        </button>
      </div>
    </div>
  )
}

export default Chatinterface
