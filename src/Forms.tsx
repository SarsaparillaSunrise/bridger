const ExerciseForm = ({item, toggleModal}) => {
  const postForm = async (formData) => {
    await postFormData({
      "id": formData.get('id'),
      "weight": formData.get('weight'),
      "reps": formData.get('reps'),
      "notes": formData.get('notes'),
    })
    toggleModal()
  }
  return (
    <>
      <h1 className="form-title">{item.name}</h1>
      <form className="entry-form" action={postForm}>
        <input name="id" type="hidden" defaultValue={item.id} readOnly />
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
        <button className="submit-form" type="submit">Submit</button>
      </form>
    </>
  );
}

const IntakeForm = ({item, toggleModal}) => {
  const postForm = async (formData) => {
    await postFormData({
      "id": formData.get('id'),
      "weight": formData.get('weight'),
    })
    toggleModal()
  }
  return (
    <>
      <h1 className="form-title">{item.name}</h1>
      <form className="entry-form" action={postForm}>
        <input name="id" type="hidden" defaultValue={item.id} readOnly />
        <p>
          <label htmlFor="weight">Weight:</label>
        </p>
        <input name="weight" type="number" min="1" inputMode="numeric" autoFocus />
        <button className="submit-form" type="submit">Submit</button>
      </form>
    </>
  );
}

const uri = 'http://127.0.0.1:80/post'
const options = {
  method: 'POST',
  mode: 'cors',
  body: null
}

const postFormData = async (formData) => {
  options["body"] = JSON.stringify(formData)
  return fetch(uri, options).then(response => response.json())
    .then(data => console.log(data.data))
    .catch(error => console.error(error));
}


export {ExerciseForm, IntakeForm}
