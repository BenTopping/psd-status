describe("Home page", () => {
  it("Contains the correct elements", () => {
    cy.intercept("v1/monitors?active=true", {
      fixture: "monitors_response.json",
    });
    cy.intercept("v1/http_records?monitor_ids=4,5,1&limit=10", {
      fixture: "http_records_response.json",
    });

    cy.visit("#/");
    cy.contains("PSD Status");
    cy.get("[data-attribute=green-systems]")
      .should("be.visible")
      .and("contain", "3 systems");
    cy.get("[data-attribute=yellow-systems]")
      .should("be.visible")
      .and("contain", "0 systems");
    cy.get("[data-attribute=red-systems]")
      .should("be.visible")
      .and("contain", "0 systems");
    cy.contains("Last updated");

    // Check there are the right number of monitors shown
    cy.get("[data-attribute=monitor-card]").should("have.length", 3);
    // Check the contents of one of the monitors
    cy.get("[data-attribute=monitor-card]")
      .first()
      .children()
      .should("contain", "Apple")
      // Response time
      .and("contain", "0.170801s")
      // Average Uptime
      .and("contain", "100.0%")
      // SSL cert expiration
      .and("contain", "Mon, 30 Oct 2023 20:25:16 GMT");
  });
});
