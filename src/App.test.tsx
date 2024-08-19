import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, test, vi } from "vitest";

import { Home, Search } from "./App";

// console.log(screen.debug());

describe("Home", () => {
  test("contains Exercise and Consumable links", async () => {
    render(
      <MemoryRouter initialEntries={[{ pathname: "/" }]}>
        <Home />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText("Exercise").toBeInTheDocument);
      expect(screen.getByText("Consumable").toBeInTheDocument);
    });
  });
});

describe("Search", () => {
  test("results contain backend exercises", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue([
        { id: 1, name: "Test Excercise 1" },
        { id: 2, name: "Test Excercise 2" },
      ]),
    });
    render(
      <MemoryRouter
        initialEntries={[{ pathname: "/search", state: "exercise" }]}
      >
        <Search />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        `${import.meta.env.VITE_UPSTREAM_ROOT}exercise`,
        {},
      );
      expect(screen.getByText("Test Excercise 1"));
      expect(screen.getByText("Test Excercise 2"));
    });
  });

  test("results contain backend consumables", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue([
        { id: 1, name: "Test Consumable 1" },
        { id: 2, name: "Test Consumable 2" },
      ]),
    });
    render(
      <MemoryRouter
        initialEntries={[{ pathname: "/search", state: "consumable" }]}
      >
        <Search />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        `${import.meta.env.VITE_UPSTREAM_ROOT}consumable`,
        {},
      );
      expect(screen.getByText("Test Consumable 1").toBeInTheDocument);
      expect(screen.getByText("Test Consumable 2").toBeInTheDocument);
    });
  });
});
