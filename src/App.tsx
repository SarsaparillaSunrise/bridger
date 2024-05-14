import { useState } from 'react'
import { ExerciseForm, BeverageForm, FoodForm} from './Forms';
import './App.css'

const lifts = [
  {
    "id": 1,
    "category": "compound-lift",
    "name": "squat",
  },
  {
    "id": 2,
    "category": "compound-lift",
    "name": "deadlift",
  },
  {
    "id": 3,
    "category": "compound-lift",
    "name": "bench press",
  }
]

const consumables = [
  {
    "id": 1,
    "category": "beverage",
    "name": "coffee",
  },
  {
    "id": 2,
    "category": "food",
    "name": "pistachio nuts",
  },
  {
    "id": 3,
    "category": "food",
    "name": "toast",
  }
]

const Home = ({clickHandler}) => {
  return (
    <div className="categories">
      <button className="category-selection" onClick={() => clickHandler('exercise')}>Exercise</button>
      <button className="category-selection" onClick={() => clickHandler('intake')}>Intake</button>
    </div>
  )
}

const formRenderer = (category, item, toggleModal) => {
  if (category === 'intake') {
    if (item.category == 'food') {
      return <FoodForm item={item} toggleModal={toggleModal} />
    }
      return <BeverageForm item={item} toggleModal={toggleModal} />
  } else {
    return <ExerciseForm item={item} toggleModal={toggleModal} />
  }
}

const Item = (category, item, modalStatus, toggleModal) => {
  return (
    <div key={item.name}>
      <button className="item-button" onClick={() => toggleModal(item.name)}>{item.name}</button>
      {
        modalStatus == item.name ?
          <div className="overlay">
          {
            formRenderer(category, item, toggleModal)
          }
          </div>
          : null
      }
    </div>
  )
}

const Search = ({category, items}) => {
  const [results, setResults] = useState(items);
  const [query, setQuery] = useState('')
  const [modalStatus, setModalStatus] = useState(null)



  const search = (e) => {
    if (/^[a-zA-Z]$/.test(e.key)) {
      const q = query + e.key;
      const matches = results.filter((match) => match.name.startsWith(q));
      setQuery(q);
      setResults(matches);
    }
    else if (e.key == 'Backspace') {
      const q = query.substring(0, query.length - 1)
      const matches = items.filter((result) => result.name.startsWith(q));
      setQuery(q)
      setResults(matches);
    }

  }

  return (
      <>
        <form className="search-form">
          <input id="search-input" name="q" autoFocus onKeyDown={search} />
        </form>
        <div className="search-results">
        <ul>
          {results.map((result) => Item(category, result, modalStatus, setModalStatus))}
        </ul>
      </div>

  </>
  )
}

const App = () => {
  const [category, setCategory] = useState(null)
  const data = {'exercise': lifts, 'intake': consumables}

  return (
      <div className="container">
        <main className="main">
          {
          category == null ?
            <Home clickHandler={setCategory}/>
          :
            <Search category={category} items={data[category]} />
          }
        </main>
      </div>
  )
}

export default App
