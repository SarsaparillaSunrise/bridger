import {Suspense, use, useState, useEffect} from "react";
import {ExerciseForm, BeverageForm, FoodForm} from "./Forms";
import "./App.css";

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
  const b = await fetch("http://127.0.0.1:8000/" + category, {mode: "cors"})
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
  const [results, setResults] = useState(items);
  const [modalStatus, setModalStatus] = useState(null);
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
          {data.map((result) => Item(result, modalStatus, setModalStatus))}
        </ul>
      </div>
    </>
  );
};


const App = () => {
  const [category, setCategory] = useState(null);
  const exercise = getItems('exercise')
  const consumable = getItems('consumable')
  const data = {'exercise': exercise, 'consumable': consumable}

  return (
    <Suspense>
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
  );
};

export default App;
