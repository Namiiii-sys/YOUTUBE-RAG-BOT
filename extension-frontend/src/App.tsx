import './index.css'
import ChatWrapper from './components/ChatUI'

const App = () => {
  return (
    <div className='w-full h-full flex flex-col bg-gray-900 text-white overflow-hidden'>
      <ChatWrapper />
    </div>
  )
}

export default App
