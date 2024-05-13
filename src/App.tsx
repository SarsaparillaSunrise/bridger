import { useState } from 'react'
import './App.css'

const Home = ({clickHandler}) => {
  return (
    <>
      <button className="category-selection" onClick={() => clickHandler('exercise')}>Exercise</button>
      <button className="category-selection" onClick={() => clickHandler('intake')}>Intake</button>
    </>
  )
}

const Search = () => (<h1>Search</h1>)

const App = () => {
  const [category, setCategory] = useState(null)

  return (
    <div className="container">
      {
      category == null ?
        <Home clickHandler={setCategory}/>
      :
        <Search />
      }

    </div>
    
  )
}

export default App
