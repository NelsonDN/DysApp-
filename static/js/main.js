/**
 * Fichier JavaScript principal pour l'application
 */

// Attendre que le DOM soit chargé
document.addEventListener("DOMContentLoaded", () => {
  // Initialiser les tooltips Bootstrap
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl))

  // Initialiser les popovers Bootstrap
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map((popoverTriggerEl) => new window.bootstrap.Popover(popoverTriggerEl))

  // Fermer automatiquement les alertes après 5 secondes
  setTimeout(() => {
    var alerts = document.querySelectorAll(".alert:not(.alert-permanent)")
    alerts.forEach((alert) => {
      var bsAlert = new window.bootstrap.Alert(alert)
      bsAlert.close()
    })
  }, 5000)

  // Ajouter la classe active aux liens de navigation correspondant à la page actuelle
  var currentLocation = window.location.pathname
  var navLinks = document.querySelectorAll(".navbar-nav .nav-link")

  navLinks.forEach((link) => {
    var href = link.getAttribute("href")
    if (href && currentLocation.startsWith(href) && href !== "/") {
      link.classList.add("active")
    }
  })
})

/**
 * Fonction pour formater le temps en minutes et secondes
 * @param {number} seconds - Nombre de secondes
 * @returns {string} - Temps formaté (ex: "2:45")
 */
function formatTime(seconds) {
  var minutes = Math.floor(seconds / 60)
  var remainingSeconds = seconds % 60

  return minutes + ":" + (remainingSeconds < 10 ? "0" : "") + remainingSeconds
}

/**
 * Fonction pour mélanger un tableau (algorithme de Fisher-Yates)
 * @param {Array} array - Tableau à mélanger
 * @returns {Array} - Tableau mélangé
 */
function shuffleArray(array) {
  var currentIndex = array.length,
    temporaryValue,
    randomIndex

  // Tant qu'il reste des éléments à mélanger
  while (0 !== currentIndex) {
    // Prendre un élément restant
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex -= 1

    // Et l'échanger avec l'élément actuel
    temporaryValue = array[currentIndex]
    array[currentIndex] = array[randomIndex]
    array[randomIndex] = temporaryValue
  }

  return array
}

/**
 * Fonction pour récupérer un cookie par son nom
 * @param {string} name - Nom du cookie
 * @returns {string|null} - Valeur du cookie ou null si non trouvé
 */
function getCookie(name) {
  var cookieValue = null
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";")
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim()
      // Le cookie commence-t-il par le nom que nous voulons?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

/**
 * Fonction pour envoyer une requête AJAX avec CSRF token
 * @param {string} url - URL de la requête
 * @param {string} method - Méthode HTTP (GET, POST, etc.)
 * @param {Object} data - Données à envoyer
 * @param {Function} successCallback - Fonction à exécuter en cas de succès
 * @param {Function} errorCallback - Fonction à exécuter en cas d'erreur
 */
function ajaxRequest(url, method, data, successCallback, errorCallback) {
  var xhr = new XMLHttpRequest()
  xhr.open(method, url, true)
  xhr.setRequestHeader("Content-Type", "application/json")
  xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"))

  xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
      var response = JSON.parse(xhr.responseText)
      successCallback(response)
    } else {
      errorCallback(xhr.statusText)
    }
  }

  xhr.onerror = () => {
    errorCallback("Erreur réseau")
  }

  xhr.send(JSON.stringify(data))
}
