import { useState } from 'react'
import './App.css'

const Home = () => {
  return (
    <h1>Home</h1>
  )
}

const Search = () => (<h1>Search</h1>)

const App = () => {
  const [category, setCategory] = useState(null)

  return (
    <div className="container">
      {
      category == null ?
        <Home />
      :
        <Search />
      }

    </div>
    
  )
}

export default App
