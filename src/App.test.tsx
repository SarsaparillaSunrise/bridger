import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, test, vi } from "vitest";

import { Form, Home, Search } from "./App";

describe("Home", () => {
  test("contains Exercise and Consumable links", async () => {
    render(
      <MemoryRouter initialEntries={[{ pathname: "/" }]}>
        <Home />
      </MemoryRouter>,
    );

    await waitFor(() => {
      // vite + pnpm + expect = https://github.com/testing-library/jest-dom/issues/567
      expect((screen.getByText("Exercise") as any).toBeInTheDocument);
      expect((screen.getByText("Consumable") as any).toBeInTheDocument);
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
      expect((screen.getByText("Test Consumable 1") as any).toBeInTheDocument);
      expect((screen.getByText("Test Consumable 2") as any).toBeInTheDocument);
    });
  });
});

describe("Form", () => {
  test("Exercise contains correct labels and fields", async () => {
    render(
      <MemoryRouter
        initialEntries={[
          {
            pathname: "/item",
            state: { name: "Test Exercise", category: "EXERCISE" },
          },
        ]}
      >
        <Form />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const volumeField = screen.getByLabelText("Volume (kg):");
      expect(volumeField).toHaveProperty("name", "volume");

      const repsField = screen.getByLabelText("Rep Count:");
      expect(repsField).toHaveProperty("name", "reps");

      const notesField = screen.getByLabelText("Notes:");
      expect(notesField).toHaveProperty("name", "notes");
    });
  });

  test("Consumable Beverage contains correct labels and fields", async () => {
    render(
      <MemoryRouter
        initialEntries={[
          {
            pathname: "/item",
            state: { name: "Test Consumable", category: "Beverage" },
          },
        ]}
      >
        <Form />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const volumeField = screen.getByLabelText("Volume (ml):");
      expect(volumeField).toHaveProperty("name", "volume");
    });
  });

  test("Consumable Food contains correct labels and fields", async () => {
    render(
      <MemoryRouter
        initialEntries={[
          {
            pathname: "/item",
            state: { name: "Test Consumable", category: "Food" },
          },
        ]}
      >
        <Form />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const volumeField = screen.getByLabelText("Volume (g):");
      expect(volumeField).toHaveProperty("name", "volume");
    });
  });
});
