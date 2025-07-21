"use client"
import { useState } from "react"
import { BsFillSendFill } from "react-icons/bs"


type ChatMessage = {
  type: "user" | "bot";
  text: string;
};

const Chatinterface = () => {
  const [chat, setchat] = useState<ChatMessage[]>([])
  const [loading, setloading] = useState(false)
  const [question, setquestion] = useState("")

  const getCurrentTabUrl = (): Promise<string> => {
  return new Promise((resolve) => {

    chrome.runtime.sendMessage({ type: "GET_CURRENT_TAB_URL" }, (response) => {
        if (chrome.runtime.lastError) {
      console.error("Error getting URL:", chrome.runtime.lastError);
    } else {
      console.log("Fetched URL from background:", response.url); // 👈 check this
    }
      resolve(response.url);
     });
     
    });
  };


  const handleAsk = async () => {
    if (!question.trim()) return;

    setloading(true);
    setchat(prev => [...prev, { type: "user", text: question }]);

    try {
      const VideoUrl = await getCurrentTabUrl();
      const res = await fetch(
        `http://localhost:8000/query?video_url=${encodeURIComponent(VideoUrl)}&question=${encodeURIComponent(question)}`,
        {
          method: "POST",
        }
      );

      const data = await res.json();
      setchat(prev => [...prev, { type: "bot", text: data.answer || "No message detected" }]);
    } catch (err) {
      console.error("Error while fetching:", err);
      setchat(prev => [...prev, { type: "bot", text: "Some error occurred" }]);
    }

    setquestion("");
    setloading(false);
  };

  return (
    <div className="w-[400px] h-[450px] px-6 py-5 overflow-hidden bg-gray-100 rounded-xl shadow-md flex flex-col">
      <h1 className="text-center text-2xl font-bold text-gray-800 mb-4">YouTube Assistant</h1>
      
      <div className="h-3/4 w-full border border-indigo-950 rounded-lg p-3 overflow-y-auto space-y-2">
        {chat.map((msg, i) => (
          <div
            key={i}
            className={`p-2 break-words whitespace-pre-wrap rounded-2xl text-sm w-fit max-w-[75%] ${msg.type === "user" ? "bg-black ml-auto text-white" : "bg-gray-300 text-black"}`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div className="text-sm text-gray-500">Loading...</div>}
      </div>

      <div className="mt-4 flex justify-between gap-2 rounded-xl border border-indigo-950 w-full">
        <input
          type="text"
          placeholder="Ask your query..."
          value={question}
          onChange={(e) => setquestion(e.target.value)}
          className="focus:outline-none w-full p-2 rounded-xl"
        />
        <button onClick={handleAsk}>
          <BsFillSendFill className="w-10 h-10 p-2" />
        </button>
      </div>
    </div>
  );
};

export default Chatinterface;
