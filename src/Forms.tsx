const ExerciseForm = ({ item, toggleModal }) => {
  const postForm = async (formData) => {
    await postFormData("workout", {
      exercise_id: formData.get("exercise_id"),
      volume: formData.get("volume"),
      reps: formData.get("reps"),
      notes: formData.get("notes"),
    });
    toggleModal();
  };
  return (
    <>
      <h1 className="form-title">{item.name}</h1>
      <span className="close-modal" onClick={toggleModal}>
        <p>&times;</p>
      </span>
      <form className="entry-form" action={postForm}>
        <input
          name="exercise_id"
          type="hidden"
          defaultValue={item.id}
          readOnly
        />
        <p>
          <label htmlFor="volume">Volume:</label>
        </p>
        <input
          name="volume"
          type="number"
          min="1"
          inputMode="numeric"
          required
          autoFocus
        />
        <p>
          <label htmlFor="reps">Rep count:</label>
        </p>
        <input name="reps" type="number" min="1" inputMode="numeric" required />
        <p>
          <label htmlFor="notes">Notes:</label>
        </p>
        <input name="notes" type="textArea" />
        <button className="submit-form" type="submit">
          Submit
        </button>
      </form>
    </>
  );
};

const FoodForm = ({ item, toggleModal }) => {
  const postForm = async (formData) => {
    await postFormData("intake", {
      consumable_id: formData.get("consumable_id"),
      volume: formData.get("volume"),
    });
    toggleModal();
  };
  return (
    <>
      <h1 className="form-title">{item.name}</h1>
      <span className="close-modal" onClick={toggleModal}>
        <p>&times;</p>
      </span>
      <form className="entry-form" action={postForm}>
        <input
          name="consumable_id"
          type="hidden"
          defaultValue={item.id}
          readOnly
        />
        <p>
          <label htmlFor="volume">Volume (g):</label>
        </p>
        <input
          name="volume"
          type="number"
          min="1"
          inputMode="numeric"
          autoFocus
        />
        <button className="submit-form" type="submit">
          Submit
        </button>
      </form>
    </>
  );
};

const BeverageForm = ({ item, toggleModal }) => {
  const postForm = async (formData) => {
    await postFormData("intake", {
      consumable_id: formData.get("consumable_id"),
      volume: formData.get("volume"),
    });
    toggleModal();
  };
  return (
    <>
      <h1 className="form-title">{item.name}</h1>
      <span className="close-modal" onClick={toggleModal}>
        <p>&times;</p>
      </span>
      <form className="entry-form" action={postForm}>
        <input
          name="consumable_id"
          type="hidden"
          defaultValue={item.id}
          readOnly
        />
        <p>
          <label htmlFor="volume">Volume (ml):</label>
        </p>
        <input
          name="volume"
          type="number"
          min="1"
          inputMode="numeric"
          autoFocus
        />
        <button className="submit-form" type="submit">
          Submit
        </button>
      </form>
    </>
  );
};

const baseUri = "http://127.0.0.1:8000/";
const postOptions = {
  method: "POST",
  mode: "cors",
  headers: {
    "Content-Type": "application/json",
  },
  body: null,
};

const getItems = async (category) =>
  fetch(baseUri + category, { mode: "cors" })
    .then((response) => response.json())
    .catch((error) => console.error(error));

const postFormData = async (category, formData) => {
  postOptions["body"] = JSON.stringify(formData);
  return fetch(baseUri + category, postOptions)
    .then((response) => response.json())
    .then((data) => console.log(data.data))
    .catch((error) => console.error(error));
};

export { ExerciseForm, FoodForm, BeverageForm, getItems };
