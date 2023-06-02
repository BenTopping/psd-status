describe("Login page", () => {
  it("Contains the correct elements", () => {
    cy.visit("#/login");
    cy.contains("PSD Status");
    cy.contains("Username");
    cy.get("[data-attribute=username-input]").should("be.visible");
    cy.contains("Password");
    cy.get("[data-attribute=password-input]").should("be.visible");
    cy.get("[data-action=login]").should("be.visible");
    // Admin navbar items should not be visible
    cy.get("[data-action=show-admin-dropdown]").should("not.exist");
  });

  it("does not login when given invalid data", () => {
    cy.intercept("v1/login", {
      statusCode: 422,
      body: {
        message: "Invalid credentials",
      },
    });
    cy.visit("#/login");
    cy.get("[data-attribute=username-input]").type("test");
    cy.get("[data-attribute=password-input]").type("invalid login");
    cy.get("[data-action=login]").click();
    // Should stay on login page
    cy.url().should("eq", "http://localhost:5173/#/login");
    // Admin navbar items should not be visible
    cy.get("[data-action=show-admin-dropdown]").should("not.exist");
    // Should have an error message
    cy.get("[data-attribute=alert]").contains(
      "Error logging in: Invalid credentials"
    );
  });

  it("Logins in correctly when given valid data", () => {
    cy.intercept("v1/login", {
      fixture: "login_response.json",
    });
    // We want to intercept the monitor polls from the homepage
    cy.intercept("v1/monitors", {
      fixture: "monitors_response.json",
    });
    cy.visit("#/login");
    cy.get("[data-attribute=username-input]").type("test");
    cy.get("[data-attribute=password-input]").type("valid login");
    cy.get("[data-action=login]").click();
    // Redirected to home page on successful login
    cy.url().should("eq", "http://localhost:5173/#/");
    // Admin navbar items should be visible
    cy.get("[data-action=show-admin-dropdown]").should("be.visible");
    // Should have a success message
    cy.get("[data-attribute=alert]").contains("Successfully logged in!");
  });
});
