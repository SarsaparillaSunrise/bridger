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
    <div className="categories">
      <button className="category-selection" onClick={() => clickHandler('exercise')}>Exercise</button>
      <button className="category-selection" onClick={() => clickHandler('intake')}>Intake</button>
    </div>
  )
}

const ExerciseForm = ({id}) => {
  const postForm = (formData) => console.log(formData)
  return (
    <form className="entry-form" action={postForm}>
      <input name="id" type="hidden" defaultValue={id} readOnly />
      <p>
        <label htmlFor="weight">Weight:</label>
      </p>
      <input name="weight" type="number" min="1" inputMode="numeric" required autoFocus />
      <p>
        <label htmlFor="reps">Rep count:</label>
      </p>
      <input name="reps" type="number" min="1" inputMode="numeric" required />
      <p>
        <label htmlFor="notes">Notes:</label>
      </p>
      <input name="notes" type="textArea" />
      <button type="submit">Submit</button>
    </form>
  );
}

const IntakeForm = ({id}) => {
  const postForm = (formData) => console.log(formData)
  return (
    <form className="entry-form" action={postForm}>
      <input name="id" type="hidden" defaultValue={id} readOnly />
      <p>
        <label htmlFor="weight">Weight:</label>
      </p>
      <input name="weight" type="number" min="1" inputMode="numeric" autoFocus />
      <button className="submit-form" type="submit">Submit</button>
    </form>
  );
}

const Item = (category, item) => {
  const [modalStatus, setModalStatus] = useState(false)
  return (
    <div key={item.name}>

    <button onClick={() => setModalStatus(!modalStatus)}>{item.name}</button>
      {
        modalStatus ?
          <div className="overlay">
          {
            category == 'exercise' ?
              <ExerciseForm />
            :
              <IntakeForm />
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
