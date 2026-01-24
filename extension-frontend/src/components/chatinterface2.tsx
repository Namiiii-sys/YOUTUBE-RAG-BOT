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
      console.log("Fetched URL from background:", response.url);
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
    <div className="w-[480px] h-[460px] px-6 py-5 overflow-hidden bg-black rounded-xl shadow-md flex flex-col">
      <h1 className="text-center text-2xl font-bold text-gray-100 mb-4">YouTube Assistant</h1>
      
      <div className="h-3/4 w-full border border-gray-200 rounded-lg p-3 overflow-y-auto space-y-2">
        {chat.map((msg, i) => (
          <div
            key={i}
            className={`p-2 break-words whitespace-pre-wrap rounded-full text-sm w-fit max-w-[75%] ${msg.type === "user" ? "bg-white ml-auto text-black" : "bg-gray-700 text-white"}`}
          >
           {msg.text.split('\n').map((line, idx) => {
              const trimmed = line.trim();

          // Numbered item (e.g., "1. something")
           if (/^\d+\.\s/.test(trimmed)) {
        return (
        <ol key={idx} className="list-decimal list-inside">
          <li>{trimmed.replace(/^\d+\.\s/, '')}</li>
        </ol>
        );
       }

       if (/^- /.test(trimmed)) {
    return (
      <ul key={idx} className="list-disc list-inside">
        <li>{trimmed.replace(/^- /, '')}</li>
      </ul>
    );
       }

      return <p key={idx} className="my-1">{trimmed}</p>;
      })}


          </div>
        ))}
        {loading && <div className="text-sm text-gray-200">Loading...</div>}
      </div>

      <div className="mt-4 flex justify-between gap-2 rounded-xl border border-white w-full">
        <input
          type="text"
          placeholder="Ask your query..."
          value={question}
          onChange={(e) => setquestion(e.target.value)}
          className="focus:outline-none w-full p-2 rounded-xl text-gray-200"
        />
        <button onClick={handleAsk}>
          <BsFillSendFill className="w-10 h-10 p-2 text-white" />
        </button>
      </div>
    </div>
  );
};

export default Chatinterface;
