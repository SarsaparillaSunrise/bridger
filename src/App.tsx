import { useState } from 'react'
import { ExerciseForm, IntakeForm} from './Forms';
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
    <div className="categories">
      <button className="category-selection" onClick={() => clickHandler('exercise')}>Exercise</button>
      <button className="category-selection" onClick={() => clickHandler('intake')}>Intake</button>
    </div>
  )
}

const Item = (category, item, modalStatus, toggleModal) => {
  return (
    <div key={item.name}>
      <button className="item-button" onClick={toggleModal}>{item.name}</button>
      {
        modalStatus ?
          <div className="overlay" onClick={toggleModal}>
          {
            category == 'exercise' ?
              <ExerciseForm item={item} toggleModal={toggleModal} />
            :
              <IntakeForm item={item} toggleModal={toggleModal} />
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
  const [modalStatus, setModalStatus] = useState(false)
  const toggleModal = () => setModalStatus(!modalStatus)



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
          <input name="q" autoFocus onKeyDown={search} />
        </form>
        <div className="search-results">
        <ul>
          {results.map((result) => Item(category, result, modalStatus, toggleModal))}
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
