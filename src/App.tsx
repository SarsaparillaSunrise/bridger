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

interface CategoryLinkProps {
  to: string;
  state: string;
  icon: string;
  children: React.ReactNode;
}

interface LoadingSpinnerProps {
  message?: string;
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
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 flex-grow flex items-center justify-center p-4">
      <div className="text-center">
        <div className="flex flex-col md:flex-row gap-6 justify-center">
          <CategoryLink to="search" state="consumable" icon="🍎">
            Consumable
          </CategoryLink>
          <CategoryLink to="search" state="exercise" icon="🏋️‍♂️">
            Exercise
          </CategoryLink>
        </div>
      </div>
    </div>
  );
};

const CategoryLink: React.FC<CategoryLinkProps> = ({
  to,
  state,
  icon,
  children,
}) => (
  <Link
    to={to}
    relative="path"
    state={state}
    className="group bg-gray-700 hover:bg-gray-600 text-gray-100 rounded-lg p-6 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
  >
    <div className="text-5xl mb-4">{icon}</div>
    <p className="text-2xl font-semibold group-hover:text-white">{children}</p>
  </Link>
);

export const Search = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-4 md:p-8">
      <ErrorBoundary
        fallback={<ErrorMessage message="Cannot connect to upstream server" />}
      >
        <Suspense fallback={<LoadingSpinner />}>
          <Items category={upstreamFetch(useLocation().state)} />
        </Suspense>
      </ErrorBoundary>
    </div>
  );
};

const Items = ({ category }: { category: Promise<Item[]> }) => {
  const items = use(category);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredResults = items.filter((match) =>
    match.name.toLowerCase().startsWith(searchTerm.toLowerCase()),
  );

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-8">
        <input
          autoFocus
          value={searchTerm}
          onChange={handleSearch}
          className="w-full text-xl text-gray-800 px-6 py-3 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white bg-opacity-90 shadow-lg transition-all duration-300"
          placeholder="Search..."
        />
      </div>
      <div className="bg-white bg-opacity-10 rounded-lg shadow-xl p-6">
        {filteredResults.length > 0 ? (
          <ul className="space-y-4">
            {filteredResults.map((item) => (
              <li
                key={item.id}
                className="transition-all duration-300 hover:bg-white hover:bg-opacity-10 rounded-lg"
              >
                <Link
                  to="/item"
                  state={item}
                  className="block text-2xl text-gray-100 py-3 px-4 hover:text-white"
                >
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-2xl text-gray-300 text-center py-8">
            No items found
          </p>
        )}
      </div>
    </div>
  );
};

export const Form = () => {
  const item = useLocation().state;
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 p-4 md:p-8">
      <div className="max-w-2xl mx-auto bg-white bg-opacity-10 rounded-lg shadow-xl p-6 md:p-8">
        <ErrorBoundary
          fallback={
            <ErrorMessage message="There was an error while submitting the form" />
          }
        >
          <Suspense fallback={<LoadingSpinner message="Submitting..." />}>
            <h1 className="text-center text-3xl md:text-4xl font-bold text-white mb-6">
              {item.name}
            </h1>
            {["Food", "Beverage"].includes(item.category) ? (
              <ConsumableForm consumable={item} />
            ) : (
              <ExerciseForm exercise={item} />
            )}
          </Suspense>
        </ErrorBoundary>
      </div>
    </div>
  );
};

const Submit = () => {
  const { pending } = useFormStatus();
  return (
    <button
      type="submit"
      disabled={pending}
      className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {pending ? "Submitting..." : "Submit"}
    </button>
  );
};

const ConsumableForm = ({ consumable }: { consumable: Consumable }) => {
  const navigate = useNavigate();
  const postConsumableForm = async (formData: FormData) => {
    "use server";
    await postFormData("intake", {
      consumable_id: formData.get("consumable_id"),
      volume: formData.get("volume"),
    });
    navigate(-1);
  };

  return (
    <form className="space-y-6" action={postConsumableForm}>
      <input
        name="consumable_id"
        type="hidden"
        defaultValue={consumable.id}
        readOnly
      />
      <div>
        <label
          htmlFor="volume-input"
          className="block text-white text-sm font-medium mb-2"
        >
          Volume ({consumable.category === "Beverage" ? "ml" : "g"}):
        </label>
        <input
          id="volume-input"
          data-testid="volume-input"
          name="volume"
          type="number"
          min="1"
          inputMode="decimal"
          required
          autoFocus
          className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <Submit />
    </form>
  );
};

const ExerciseForm = ({ exercise }: { exercise: Exercise }) => {
  const navigate = useNavigate();
  const postExerciseForm = async (formData: FormData) => {
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
    <form className="space-y-6" action={postExerciseForm}>
      <input
        name="exercise_id"
        type="hidden"
        defaultValue={exercise.id}
        readOnly
      />
      <div>
        <label
          htmlFor="volume-input"
          className="block text-white text-sm font-medium mb-2"
        >
          Volume (kg):
        </label>
        <input
          id="volume-input"
          name="volume"
          type="number"
          min="1"
          inputMode="decimal"
          required
          autoFocus
          className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label
          htmlFor="reps-input"
          className="block text-white text-sm font-medium mb-2"
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
          className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label
          htmlFor="notes-input"
          className="block text-white text-sm font-medium mb-2"
        >
          Notes:
        </label>
        <textarea
          id="notes-input"
          name="notes"
          rows={3}
          className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        ></textarea>
      </div>
      <Submit />
    </form>
  );
};

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = "Loading...",
}) => (
  <div className="flex flex-col items-center justify-center h-64">
    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div>
    <p className="text-white text-lg">{message}</p>
  </div>
);

const ErrorMessage = ({ message }: { message: string }) => (
  <div
    className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg"
    role="alert"
  >
    <p className="font-bold">Error</p>
    <p>{message}</p>
  </div>
);

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
