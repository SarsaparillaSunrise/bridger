import { Suspense, use } from "react";
import { preconnect, useFormStatus } from "react-dom";
import { ErrorBoundary } from "react-error-boundary";
import {
  Link,
  RouterProvider,
  createBrowserRouter,
  useLocation,
  useNavigate,
} from "react-router-dom";

import "./index.css";

const upstreamRoot = "http://127.0.0.1:8000/";

const postOptions = {
  method: "POST",
  mode: "cors",
  headers: {
    "Content-Type": "application/json",
  },
  body: null,
};

const upstreamFetch = async (endpoint: string, postOptions = {}) => {
  const res = await fetch(`${upstreamRoot}${endpoint}`, postOptions);
  return res.json();
};

const postFormData = async (endpoint, formData) => {
  postOptions["body"] = JSON.stringify(formData);
  return upstreamFetch(endpoint, postOptions);
};

export const Home = () => {
  return (
    <div id="category-list">
      <p>
        <Link
          to="search"
          relative="path"
          state="consumable"
          className="category-link"
        >
          Consumable
        </Link>
      </p>
      <p>
        <Link
          to="search"
          relative="path"
          state="exercise"
          className="category-link"
        >
          Exercise
        </Link>
      </p>
    </div>
  );
};

export const Search = () => {
  return (
    <ErrorBoundary fallback={<p>Can't connect to upstream server</p>}>
      <Suspense fallback={<p>⌛Downloading...</p>}>
        <Items category={upstreamFetch(useLocation().state)} />
      </Suspense>
    </ErrorBoundary>
  );
};

const Items = ({ category: category }) => {
  const items = use(category);
  return (
    <div className="search-results">
      <ul>
        {items.length
          ? items.map((item) => (
              <li key={item.id}>
                <Link to="/item" state={item}>
                  {item.name}
                </Link>{" "}
              </li>
            ))
          : "No items"}
      </ul>
    </div>
  );
};

export const Form = () => {
  const item = useLocation().state;
  return (
    <>
      <ErrorBoundary
        fallback={<p>There was an error while submitting the form</p>}
      >
        <Suspense fallback="Submitting...">
          <h1 className="form-title">{item.name}</h1>
          {["FOOD", "BEVERAGE"].includes(item.category) ? (
            <ConsumableForm consumable={item} />
          ) : (
            <ExerciseForm exercise={item} />
          )}
        </Suspense>
      </ErrorBoundary>
    </>
  );
};

const Submit = () => {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
};

const ConsumableForm = ({ consumable }) => {
  const navigate = useNavigate();
  const postConsumableForm = async (formData) => {
    "use server";
    await postFormData("intake", {
      consumable_id: formData.get("consumable_id"),
      volume: formData.get("volume"),
    });
    navigate("/");
  };

  return (
    <form className="entry-form" action={postConsumableForm}>
      <input
        name="consumable_id"
        type="hidden"
        defaultValue={consumable.id}
        readOnly
      />
      <p>
        <label htmlFor="volume">
          Volume ({consumable.category == "BEVERAGE" ? "ml" : "g"}):
        </label>
      </p>
      <input
        name="volume"
        type="number"
        min="1"
        inputMode="numeric"
        required
        autoFocus
      />
      <Submit />
    </form>
  );
};

const ExerciseForm = ({ exercise }) => {
  const navigate = useNavigate();
  const postExerciseForm = async (formData) => {
    "use server";
    // await postFormData("workout", {
    //   exercise_id: formData.get("exercise_id"),
    //   volume: formData.get("volume"),
    //   reps: formData.get("reps"),
    //   notes: formData.get("notes"),
    // });
    navigate("/");
  };

  return (
    <div>
      <ErrorBoundary
        fallback={<p>There was an error while submitting the form</p>}
      >
        <form className="entry-form" action={postExerciseForm}>
          <input
            name="exercise_id"
            type="hidden"
            defaultValue={exercise.id}
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
          <input
            name="reps"
            type="number"
            min="1"
            inputMode="numeric"
            required
          />
          <p>
            <label htmlFor="notes">Notes:</label>
          </p>
          <input name="notes" type="textArea" />
          <Submit />
        </form>
      </ErrorBoundary>
    </div>
  );
};

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/search",
    element: <Search />,
  },
  {
    path: "/item",
    element: <Form />,
  },
]);

export default function App() {
  preconnect(upstreamRoot);
  return <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />;
}

if (import.meta.hot) {
  import.meta.hot.dispose(() => router.dispose());
}
