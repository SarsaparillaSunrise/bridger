import {Suspense, use, useState, useEffect} from "react";
import {ExerciseForm, BeverageForm, FoodForm} from "./Forms";
import { ErrorBoundary } from "react-error-boundary";
import "./App.css";

const upstreamRoot = import.meta.env.VITE_UPSTREAM_ROOT

const Home = ({clickHandler}) => {
  return (
    <div className="categories">
      <button
        className="category-selection"
        onClick={() => clickHandler("exercise")}
      >
        Exercise
      </button>
      <button
        className="category-selection"
        onClick={() => clickHandler("consumable")}
      >
        Consumable
      </button>
    </div>
  );
};




const formRenderer = (item, toggleModal) => {
  if (item.category == "Food") {
    return <FoodForm item={item} toggleModal={toggleModal} />;
  } else if (item.category == "Beverage") {
    return <BeverageForm item={item} toggleModal={toggleModal} />;
  } else {
    return <ExerciseForm item={item} toggleModal={toggleModal} />;
  }
};

const getItems = async (category) => {
  const b = await fetch(upstreamRoot + category, {mode: "cors"})
  return b.json()
}

const Item = (item, modalStatus, toggleModal) => {
  return (
    <div key={item.name}>
      <button className="item-button" onClick={() => toggleModal(item.name)}>
        {item.name}
      </button>
      {modalStatus == item.name ? (
        <div className="overlay">{formRenderer(item, toggleModal)}</div>
      ) : null}
    </div>
  );
};

const Search = ({items}) => {
  const [results, setResults] = useState([]);
  const [modalStatus, setModalStatus] = useState(null);
  // TODO: reduce variables and migrate to reducer
  const data = use(items);

  const search = (e) =>
    setResults(
      data.filter((match) =>
        match.name.toLowerCase().startsWith(e.target.value.toLowerCase()),
      ),
    );

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
  );
};


const App = () => {
  const [category, setCategory] = useState(null);
  const data = {'exercise': getItems('exercise'), 'consumable': getItems('consumable')}

  return (

  <ErrorBoundary fallback={<p>Can't connect to upstream server</p>}>
    <Suspense fallback={<p>Downloading...</p>}>
      <div className="container">
        <main className="main">
          {category == null ? (
            <Home clickHandler={setCategory} />
          ) : (
            <Search items={data[category]} />
          )}
        </main>
      </div>
    </Suspense>
    </ErrorBoundary>
  );
};

export default App;
