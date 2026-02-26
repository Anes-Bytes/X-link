(function () {
  function setStatus(statusEl, message, type) {
    statusEl.textContent = message;
    statusEl.classList.remove("is-ok", "is-error");
    if (type) {
      statusEl.classList.add(type);
    }
  }

  function toMessage(reason) {
    if (reason === "ok") return "Available";
    if (reason === "taken") return "Already taken";
    if (reason === "reserved") return "Reserved name";
    if (reason === "invalid_format") return "Invalid format";
    return "Unavailable";
  }

  function bindChecker(input, statusEl) {
    if (!input || !statusEl) return;
    var checkUrl = statusEl.dataset.checkUrl || "/api/check-subdomain/";
    var debounceTimer = null;

    function updateStatus(message, type) {
      setStatus(statusEl, message, type);
    }

    function checkSubdomain(name) {
      if (!name) {
        updateStatus("", null);
        return;
      }

      fetch(checkUrl + "?name=" + encodeURIComponent(name), {
        method: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          var type = data.available ? "is-ok" : "is-error";
          updateStatus(toMessage(data.reason), type);
        })
        .catch(function () {
          updateStatus("Could not verify right now", "is-error");
        });
    }

    input.addEventListener("input", function (event) {
      var name = event.target.value.trim().toLowerCase();
      event.target.value = name;
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        checkSubdomain(name);
      }, 500);
    });
  }

  var mainInput = document.getElementById("id_username");
  var mainStatus = document.getElementById("subdomain-status");
  if (mainInput && mainStatus) {
    bindChecker(mainInput, mainStatus);
  }

  var dynamicInputs = document.querySelectorAll(".js-subdomain-input[data-status-target]");
  dynamicInputs.forEach(function (input) {
    var statusId = input.getAttribute("data-status-target");
    var statusEl = document.getElementById(statusId);
    if (statusEl) {
      bindChecker(input, statusEl);
    }
  });
})();
