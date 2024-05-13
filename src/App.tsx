import { useState } from 'react'
import './App.css'

const lifts = [
  {
    "id": 1,
    "name": "squat",
  },
  {
    "id": 2,
    "name": "deadlift",
  },
  {
    "id": 3,
    "name": "bench press",
  }
]

const foods = [
  {
    "id": 1,
    "name": "coffee",
  },
  {
    "id": 2,
    "name": "pistachio nuts",
  },
  {
    "id": 3,
    "name": "toast",
  }
]

const Home = ({clickHandler}) => {
  return (
    <>
      <button className="category-selection" onClick={() => clickHandler('exercise')}>Exercise</button>
      <button className="category-selection" onClick={() => clickHandler('intake')}>Intake</button>
    </>
  )
}

const Search = ({category, items}) => {
  return (
  <>
    <h1>Search</h1>
    <h2>{category}</h2>
    <h2>{JSON.stringify(items)}</h2>
  </>
  )
}

const App = () => {
  const [category, setCategory] = useState(null)
  const data = {'exercise': lifts, 'intake': foods}

  return (
    <div className="container">
      {
      category == null ?
        <Home clickHandler={setCategory}/>
      :
        <Search category={category} items={data[category]} />
      }

    </div>
    
  )
}

export default App
