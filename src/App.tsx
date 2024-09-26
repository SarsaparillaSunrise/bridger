import { Suspense, use, useState } from "react";
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

interface Item {
  id: number;
  name: string;
}

interface Consumable {
  id: number;
  name: string;
  category: string;
}

interface Exercise {
  id: number;
  name: string;
}

const upstreamRoot = import.meta.env.VITE_UPSTREAM_ROOT;
const postOptions: RequestInit = {
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

const postFormData = async (
  endpoint: string,
  formData: Record<string, unknown>,
) => {
  postOptions["body"] = JSON.stringify(formData);
  return upstreamFetch(endpoint, postOptions);
};
export const Home = () => {
  return (
    <div
      id="category-list"
      className="gap-x-3 text-center text-5xl text-gray-200"
    >
      <div className="p-5 bg-transparent text-grey-200 font-semibold hover:text-white">
        <p>
          <Link to="search" relative="path" state="consumable">
            Consumable
          </Link>
        </p>
      </div>
      <div className="p-5 bg-transparent text-grey-200 font-semibold hover:text-white">
        <p className="p-3">
          <Link to="search" relative="path" state="exercise">
            Exercise
          </Link>
        </p>
      </div>
    </div>
  );
};

export const Search = () => {
  return (
    <ErrorBoundary fallback={<p>Cannot connect to upstream server</p>}>
      <Suspense fallback={<p>⌛Downloading...</p>}>
        <Items category={upstreamFetch(useLocation().state)} />
      </Suspense>
    </ErrorBoundary>
  );
};

const Items = ({ category }: { category: Promise<Item[]> }) => {
  const items = use(category);
  const [searchTerm, setSearchTerm] = useState("");
  const data = use(category);

  const filteredResults = data.filter((match) =>
    match.name.toLowerCase().startsWith(searchTerm.toLowerCase()),
  );

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <>
      <div className="w-full">
        <input
          autoFocus
          value={searchTerm}
          onChange={handleSearch}
          className="block w-full text-3xl text-gray-800 px-4 py-2 rounded-full focus:outline-none my-5 focus:ring-2 focus:ring-blue-500"
          placeholder="Search..."
        />
      </div>
      <div className="w-full">
        <ul className="text-5xl space-y-4">
          {items.length ? (
            filteredResults.map((item) => (
              <li key={item.id}>
                <Link to="/item" state={item}>
                  {item.name}
                </Link>{" "}
              </li>
            ))
          ) : (
            <li>No items</li>
          )}
        </ul>
      </div>
    </>
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
          <h1 className="text-center text-5xl space-y-4">{item.name}</h1>
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
    <button
      type="submit"
      disabled={pending}
      className="bg-blue-500 hover:bg-blue-700 mt-3 text-white font-bold py-2 px-4 rounded-full float-right"
    >
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
};

const ConsumableForm = ({ consumable }: { consumable: Consumable }) => {
  const navigate = useNavigate();
  const postConsumableForm = async (formData: any) => {
    "use server";
    await postFormData("intake", {
      consumable_id: formData.get("consumable_id"),
      volume: formData.get("volume"),
    });
    navigate(-1);
  };

  return (
    <form className="entry-form" action={postConsumableForm}>
      <input
        name="consumable_id"
        type="hidden"
        defaultValue={consumable.id}
        readOnly
      />
      <label className="block text-white-700 font-bold my-2">
        Volume ({consumable.category == "BEVERAGE" ? "ml" : "g"}):
        <input
          data-testid="volume-input"
          name="volume"
          type="number"
          min="1"
          inputMode="decimal"
          required
          autoFocus
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </label>
      <Submit />
    </form>
  );
};

const ExerciseForm = ({ exercise }: { exercise: Exercise }) => {
  const navigate = useNavigate();
  const postExerciseForm = async (formData: any) => {
    "use server";
    await postFormData("workout", {
      exercise_id: formData.get("exercise_id"),
      volume: formData.get("volume"),
      reps: formData.get("reps"),
      notes: formData.get("notes"),
    });
    navigate(-1);
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
            <label
              htmlFor="volume-input"
              className="block text-white-700 font-bold my-2"
            >
              Volume (kg):
            </label>
          </p>
          <input
            id="volume-input"
            name="volume"
            type="number"
            min="1"
            inputMode="decimal"
            required
            autoFocus
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
          <p>
            <label
              htmlFor="reps-input"
              className="block text-white-700 font-bold my-2"
            >
              Rep Count:
            </label>
            <input
              id="reps-input"
              name="reps"
              type="number"
              min="1"
              inputMode="decimal"
              required
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          </p>
          <p>
            <label
              htmlFor="notes-input"
              className="block text-white-700 font-bold my-2"
            >
              Notes:
            </label>
          </p>
          <input
            id="notes-input"
            name="notes"
            type="textArea"
            className="shadow appearance-none border rounded w-full py-2 px-3 h-20 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
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
