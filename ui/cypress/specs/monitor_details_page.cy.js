describe("Monitors page", () => {
  it("Contains the correct elements", () => {
    cy.intercept("v1/monitors?ids=1", {
      fixture: "monitor_response.json",
    });
    cy.intercept("v1/http_records?monitor_ids=1", {
      fixture: "monitor_http_records_response.json",
    });
    cy.intercept("v1/protocols", {
      fixture: "protocols_response.json",
    });

    cy.visit("#/monitor/1");

    // Check first monitor header has correct content
    cy.get("[data-attribute=monitor-header]")
      .should("contain", "Google")
      // Protocol
      .and("contain", "https")
      // Target
      .and("contain", "google.com")
      // Delay
      .and("contain", "300s")
      // SSL Expiry
      .and("contain", "Mon, 30 Oct 2023 20:25:16 GMT")
      // Average uptime
      .and("contain", "100.0%")
      // Last response time
      .and("contain", "0s");
    // Check correct status colour is shown
    cy.get("[data-attribute=monitor-status]").should(
      "have.class",
      "bg-red-400"
    );

    // Check status table contains correct information
    cy.contains("Incidents");
    cy.get("[data-attribute=status-table]")
      // id
      .should("contain", "21")
      // Error
      .and("contain", "There was an error")
      // created_at
      .and("contain", "2023-05-05 14:31:13");

    // Check response time graph
    cy.get("#response-time-chart").should("be.visible");
  });
});
