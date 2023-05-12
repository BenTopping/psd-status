describe("Monitors page", () => {
  beforeEach(() => {
    // We need to login because it is an authenticated route
    cy.login();
  });

  it("Contains the correct elements", () => {
    cy.intercept("/monitors", {
      fixture: "monitors_response.json",
    });
    cy.intercept("/protocols", {
      fixture: "protocols_response.json",
    });

    cy.visit("#/monitors");
    cy.contains("Monitors");
    cy.get("[data-attribute=monitor-item]").should("have.length", 3);
    // Check first monitor item has correct content
    cy.get("[data-attribute=monitor-item]")
      .first()
      .children()
      .should("contain", "Apple")
      // Protocol
      .and("contain", "https")
      // Target
      .and("contain", "apple.com");

    cy.contains("New");
    cy.get("[data-action=select-new-monitor]").should("be.visible");
    cy.get("[data-attribute=monitor-edit]").should("be.visible");
    // Check monitor edit has correct labels
    cy.get("[data-attribute=monitor-edit]")
      // Monitor name
      .should("contain", "Name")
      // Protocol selection
      .and("contain", "Protocol")
      // Target
      .and("contain", "Target")
      // Poll interval
      .and("contain", "Poll delay")
      // Active
      .and("contain", "Active");
    cy.get("[data-action=submit-monitor]").should("be.visible");
  });

  it("Can create a new monitor", () => {
    cy.intercept("/monitors", {
      fixture: "monitors_response.json",
    });
    cy.intercept("/protocols", {
      fixture: "protocols_response.json",
    });
    cy.intercept('/monitor', {
      statusCode: 200,
      body: {
        message: 'Successful',
      },
    })

    cy.visit("#/monitors");
    cy.get("[data-attribute=name-input]").type("NewMonitor");
    cy.get("[data-attribute=protocol-select]").select("http");
    cy.get("[data-attribute=target-input]").type("www.newMonitor.com");
    cy.get("[data-attribute=delay-select]").select("5m");
    cy.get("[data-attribute=active-select]").select("True");

    cy.intercept("/monitors", {
      fixture: "updated_monitors_response.json",
    });

    cy.get("[data-action=submit-monitor]").click();

    // Check monitor shows up in list
    cy.get("[data-attribute=monitor-item]")
      .last()
      .children()
      .should("contain", "NewMonitor")
      // Protocol
      .and("contain", "http")
      // Target
      .and("contain", "www.newMonitor.com");
  });

  it("Can update a monitor", () => {
    cy.intercept("/monitors", {
      fixture: "monitors_response.json",
      times: 1
    });
    cy.intercept("/protocols", {
      fixture: "protocols_response.json",
    });
    cy.intercept('/monitor', {
      statusCode: 200,
      body: {
        message: 'Successful',
      },
    })

    cy.visit("#/monitors");
    cy.get("[data-attribute=monitor-item]").first().click();
    cy.get("[data-attribute=protocol-select]").select("https");

    cy.intercept("/monitors", {
      fixture: "updated_monitors_response.json",
      times: 1
    });

    cy.get("[data-action=submit-monitor]").click();

    // Check monitor is updated in list
    cy.get("[data-attribute=monitor-item]")
      .first()
      .children()
      .should("contain", "Apple")
      // Protocol (updated)
      .and("contain", "http")
      // Target
      .and("contain", "apple.com");
  });
});
