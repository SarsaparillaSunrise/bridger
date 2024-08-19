import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, test, vi } from "vitest";

import { Search } from "./App";

// console.log(screen.debug());

describe("Search", () => {
  test("backend response exercises are present in search results", async () => {
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

  test("backend response consumables are present in search results", async () => {
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
      expect(screen.getByText("Test Consumable 1"));
      expect(screen.getByText("Test Consumable 2"));
    });
  });
});
