import './index.css'
import ChatWrapper from './components/ChatUI'

const App = () => {
  return (
    <div className='w-[500px] h-[500px] flex flex-col bg-gray-900 text-white overflow-hidden'>
      <ChatWrapper />
    </div>
  )
}

export default App
