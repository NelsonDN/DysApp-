// /**
//  * Gestion du mode dyslexie
//  */

// document.addEventListener("DOMContentLoaded", () => {
//   // Récupérer l'interrupteur du mode dyslexie
//   var dyslexiaModeSwitch = document.getElementById("dyslexiaModeSwitch")

//   if (dyslexiaModeSwitch) {
//     // Ajouter un événement de changement
//     dyslexiaModeSwitch.addEventListener("change", function () {
//       toggleDyslexiaMode(this.checked)
//     })
//   }
// })

// /**
//  * Active ou désactive le mode dyslexie
//  * @param {boolean} enabled - Indique si le mode dyslexie doit être activé
//  */
// function toggleDyslexiaMode(enabled) {
//   // Envoyer une requête AJAX pour mettre à jour la préférence de l'utilisateur
//   var ajaxRequest = (url, method, data, successCallback, errorCallback) => {
//     var xhr = new XMLHttpRequest()
//     xhr.open(method, url, true)
//     xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
//     xhr.onreadystatechange = () => {
//       if (xhr.readyState === 4) {
//         if (xhr.status >= 200 && xhr.status < 300) {
//           successCallback(JSON.parse(xhr.responseText))
//         } else {
//           errorCallback(xhr.statusText)
//         }
//       }
//     }
//     xhr.send(JSON.stringify(data))
//   }

//   ajaxRequest(
//     "/accounts/toggle-dyslexia-mode/",
//     "POST",
//     { dyslexia_mode: enabled },
//     (response) => {
//       if (response.status === "success") {
//         // Recharger la page pour appliquer les changements
//         location.reload()
//       } else {
//         console.error("Erreur lors de la mise à jour du mode dyslexie:", response.message)
//         alert("Une erreur est survenue lors de la mise à jour du mode dyslexie.")
//       }
//     },
//     (error) => {
//       console.error("Erreur lors de la mise à jour du mode dyslexie:", error)
//       alert("Une erreur est survenue lors de la mise à jour du mode dyslexie.")
//     },
//   )
// }
/**
 * Gestion du mode dyslexie
 */

document.addEventListener("DOMContentLoaded", () => {
  // Récupérer l'interrupteur du mode dyslexie
  var dyslexiaModeSwitch = document.getElementById("dyslexiaModeSwitch");

  if (dyslexiaModeSwitch) {
    // Ajouter un événement de changement
    dyslexiaModeSwitch.addEventListener("change", function () {
      toggleDyslexiaMode(this.checked);
    });
  }
});

/**
 * Active ou désactive le mode dyslexie
 * @param {boolean} enabled - Indique si le mode dyslexie doit être activé
 */
function toggleDyslexiaMode(enabled) {
  // Envoyer une requête AJAX pour mettre à jour la préférence de l'utilisateur
  fetch("/accounts/toggle-dyslexia-mode/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({ dyslexia_mode: enabled })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === "success") {
      // Recharger la page pour appliquer les changements
      location.reload();
    } else {
      console.error("Erreur lors de la mise à jour du mode dyslexie:", data.message);
      alert("Une erreur est survenue lors de la mise à jour du mode dyslexie.");
    }
  })
  .catch(error => {
    console.error("Erreur lors de la mise à jour du mode dyslexie:", error);
    alert("Une erreur est survenue lors de la mise à jour du mode dyslexie.");
  });
}

/**
 * Récupère un cookie par son nom
 * @param {string} name - Nom du cookie
 * @returns {string|null} - Valeur du cookie ou null si non trouvé
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}