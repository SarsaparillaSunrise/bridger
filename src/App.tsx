import { useState, useEffect } from 'react'
import { ExerciseForm, BeverageForm, FoodForm, getItems} from './Forms';
import './App.css'


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
  const [modalStatus, setModalStatus] = useState(null)

  const search = (e) => setResults(items.filter((match) => match.name.startsWith(e.target.value)));

  return (
    <>
      <form className="search-form">
        <input id="search-input" name="q" autoFocus onChange={search} />
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
  const [data, setData] = useState()

  // TODO: Find out why this runs twice
  useEffect(() => {
    const fetchData = async () => 
      setData({'exercise': await getItems('exercise'), 'intake': await getItems('intake')});

    fetchData()
        .catch(console.error);;
    }, [])

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
