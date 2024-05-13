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

const Item = (item) => (<h3 key={item.name}>{item.name}</h3>)

const Search = ({category, items}) => {
  const search = (e) => console.log(e.key)
  return (
      <>
        <form className="search-form">
          <input name="q" autoFocus onKeyDown={search} />
        </form>
        <div className="search-results">
        <ul>
          {items.map((item) => Item(item))}
        </ul>
      </div>

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
