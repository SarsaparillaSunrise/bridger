import { useState, useEffect } from 'react'
import { ExerciseForm, BeverageForm, FoodForm, getItems} from './Forms';
import './App.css'


const Home = ({clickHandler}) => {
  return (
    <div className="categories">
      <button className="category-selection" onClick={() => clickHandler('exercise')}>Exercise</button>
      <button className="category-selection" onClick={() => clickHandler('consumable')}>Consumable</button>
    </div>
  )
}

const formRenderer = (item, toggleModal) => {
    if (item.category == 'Food') {
      return <FoodForm item={item} toggleModal={toggleModal} />
    } else if (item.category == 'Beverage') {
      return <BeverageForm item={item} toggleModal={toggleModal} />
    } else {
    return <ExerciseForm item={item} toggleModal={toggleModal} />
  }
}

const Item = (item, modalStatus, toggleModal) => {
  return (
    <div key={item.name}>
      <button className="item-button" onClick={() => toggleModal(item.name)}>{item.name}</button>
      {
        modalStatus == item.name ?
          <div className="overlay">
          {
            formRenderer(item, toggleModal)
          }
          </div>
          : null
      }
    </div>
  )
}

const Search = ({items}) => {
  const [results, setResults] = useState(items);
  const [modalStatus, setModalStatus] = useState(null)

  const search = (e) => setResults(items.filter(
    (match) => match.name.toLowerCase() .startsWith(e.target.value.toLowerCase())));

  return (
    <>
      <form className="search-form">
        <input id="search-input" name="q" autoFocus onChange={search} />
      </form>
      <div className="search-results">
        <ul>
          {results.map((result) => Item(result, modalStatus, setModalStatus))}
        </ul>
      </div>
    </>
  )
}

const App = () => {
  const [category, setCategory] = useState(null)
  const [data, setData] = useState()

  // TODO: Check this doesn't run twice in prod
  useEffect(() => {
    const fetchData = async () => 
      setData({'exercise': await getItems('exercise'), 'consumable': await getItems('consumable')});

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
            <Search items={data[category]} />
          }
        </main>
      </div>
  )
}

export default App
