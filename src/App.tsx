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

const Item = (category, item) => {
  const [modalStatus, setModalStatus] = useState(false)
  const toggleModal = () => setModalStatus(!modalStatus)

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
          : ''
      }
    </div>
  )
}

const Search = ({category, items}) => {
  const search = (e) => console.log(e.key)
  return (
      <>
        <form className="search-form">
          <input name="q" autoFocus onKeyDown={search} />
        </form>
        <div className="search-results">
        <ul>
          {items.map((item) => Item(category, item))}
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
