/**
 * Dyslexia Tools - JavaScript utilities for dyslexia exercises
 */

// Text to Speech functionality
class TextToSpeech {
  constructor() {
    this.synth = window.speechSynthesis
    this.voice = null
    this.rate = 0.9
    this.pitch = 1
    this.volume = 1
    this.lang = "fr-FR"

    // Initialize voices
    this.initVoices()
  }

  initVoices() {
    // Get available voices
    let voices = this.synth.getVoices()

    // If voices are not loaded yet, wait for them
    if (voices.length === 0) {
      window.speechSynthesis.addEventListener("voiceschanged", () => {
        voices = this.synth.getVoices()
        this.setVoice()
      })
    } else {
      this.setVoice()
    }
  }

  setVoice() {
    const voices = this.synth.getVoices()

    // Try to find a French voice
    this.voice = voices.find((voice) => voice.lang.includes("fr"))

    // If no French voice is found, use the first available voice
    if (!this.voice && voices.length > 0) {
      this.voice = voices[0]
    }
  }

  speak(text) {
    // Cancel any ongoing speech
    this.synth.cancel()

    // Create a new utterance
    const utterance = new SpeechSynthesisUtterance(text)

    // Set properties
    utterance.voice = this.voice
    utterance.rate = this.rate
    utterance.pitch = this.pitch
    utterance.volume = this.volume
    utterance.lang = this.lang

    // Speak
    this.synth.speak(utterance)

    return utterance
  }

  stop() {
    this.synth.cancel()
  }

  pause() {
    this.synth.pause()
  }

  resume() {
    this.synth.resume()
  }

  // Highlight text as it's being spoken
  speakWithHighlight(text, element) {
    // Split text into words
    const words = text.split(" ")

    // Create a span for each word
    const html = words.map((word) => `<span class="tts-word">${word}</span>`).join(" ")

    // Set the HTML
    element.innerHTML = html

    // Get all word spans
    const wordSpans = element.querySelectorAll(".tts-word")

    // Create utterance
    const utterance = this.speak(text)

    // Track current word
    let currentWordIndex = 0

    // Add event listeners
    utterance.onboundary = (event) => {
      if (event.name === "word") {
        // Remove highlight from previous word
        if (currentWordIndex > 0) {
          wordSpans[currentWordIndex - 1].classList.remove("highlight")
        }

        // Add highlight to current word
        if (currentWordIndex < wordSpans.length) {
          wordSpans[currentWordIndex].classList.add("highlight")
          currentWordIndex++
        }
      }
    }

    utterance.onend = () => {
      // Remove all highlights
      wordSpans.forEach((span) => span.classList.remove("highlight"))
    }
  }
}

// Syllable highlighter
class SyllableHighlighter {
  constructor() {
    this.syllablePatterns = [
      // Common French syllable patterns
      /([bcdfghjklmnpqrstvwxz]*[aeiouy]+)/gi,
      /([bcdfghjklmnpqrstvwxz]+[aeiouy]+[bcdfghjklmnpqrstvwxz]+)/gi,
    ]
  }

  // Split a word into syllables
  splitIntoSyllables(word) {
    const syllables = []
    let remainingWord = word

    // Apply patterns
    for (const pattern of this.syllablePatterns) {
      const matches = remainingWord.match(pattern)

      if (matches) {
        for (const match of matches) {
          const index = remainingWord.indexOf(match)

          if (index > 0) {
            syllables.push(remainingWord.substring(0, index))
          }

          syllables.push(match)
          remainingWord = remainingWord.substring(index + match.length)
        }
      }
    }

    // Add any remaining part
    if (remainingWord.length > 0) {
      syllables.push(remainingWord)
    }

    return syllables
  }

  // Highlight syllables in a text
  highlightSyllables(text, element) {
    // Split text into words
    const words = text.split(" ")

    // Process each word
    const processedWords = words.map((word) => {
      // Skip punctuation and special characters
      if (!/[a-zA-Z]/.test(word)) {
        return word
      }

      // Split word into syllables
      const syllables = this.splitIntoSyllables(word)

      // Create HTML with syllables
      return syllables.map((syllable) => `<span class="syllable">${syllable}</span>`).join("")
    })

    // Set the HTML
    element.innerHTML = processedWords.join(" ")

    // Add event listeners to syllables
    const syllableElements = element.querySelectorAll(".syllable")

    syllableElements.forEach((syllable) => {
      syllable.addEventListener("mouseover", () => {
        syllable.classList.add("syllable-highlight")
      })

      syllable.addEventListener("mouseout", () => {
        syllable.classList.remove("syllable-highlight")
      })

      syllable.addEventListener("click", () => {
        // Create TTS instance and speak the syllable
        const tts = new TextToSpeech()
        tts.speak(syllable.textContent)
      })
    })
  }
}

// Letter highlighter
class LetterHighlighter {
  constructor() {
    // Map of similar-looking letters
    this.similarLetters = {
      b: ["d", "p"],
      d: ["b", "p", "q"],
      p: ["b", "d", "q"],
      q: ["d", "p"],
      m: ["n", "w"],
      n: ["m", "u"],
      u: ["n", "v"],
      v: ["u", "w"],
      w: ["m", "v"],
    }
  }

  // Highlight letters in a text
  highlightLetters(text, element) {
    // Split text into characters
    const characters = text.split("")

    // Create HTML with letters
    const html = characters
      .map((char) => {
        if (char === " ") {
          return " "
        } else {
          return `<span class="letter-container" data-letter="${char.toLowerCase()}">${char}</span>`
        }
      })
      .join("")

    // Set the HTML
    element.innerHTML = html

    // Add event listeners to letters
    const letterElements = element.querySelectorAll(".letter-container")

    letterElements.forEach((letter) => {
      letter.addEventListener("mouseover", () => {
        letter.classList.add("letter-highlight")

        // Highlight similar letters
        const letterValue = letter.getAttribute("data-letter")
        const similarLetters = this.similarLetters[letterValue] || []

        letterElements.forEach((otherLetter) => {
          const otherLetterValue = otherLetter.getAttribute("data-letter")

          if (similarLetters.includes(otherLetterValue)) {
            otherLetter.classList.add("letter-similar")
          }
        })
      })

      letter.addEventListener("mouseout", () => {
        letter.classList.remove("letter-highlight")

        // Remove highlight from similar letters
        letterElements.forEach((otherLetter) => {
          otherLetter.classList.remove("letter-similar")
        })
      })

      letter.addEventListener("click", () => {
        // Create TTS instance and speak the letter
        const tts = new TextToSpeech()
        tts.speak(letter.textContent)
      })
    })
  }
}

// Drag and drop functionality
class DragDropManager {
  constructor(dragItems, dropZones, onDrop) {
    this.dragItems = dragItems
    this.dropZones = dropZones
    this.onDrop = onDrop

    this.init()
  }

  init() {
    // Initialize drag items
    this.dragItems.forEach((item) => {
      item.setAttribute("draggable", "true")

      item.addEventListener("dragstart", (e) => {
        e.dataTransfer.setData("text/plain", item.getAttribute("data-id"))
        item.classList.add("dragging")
      })

      item.addEventListener("dragend", () => {
        item.classList.remove("dragging")
      })
    })

    // Initialize drop zones
    this.dropZones.forEach((zone) => {
      zone.addEventListener("dragover", (e) => {
        e.preventDefault()
        zone.classList.add("active")
      })

      zone.addEventListener("dragleave", () => {
        zone.classList.remove("active")
      })

      zone.addEventListener("drop", (e) => {
        e.preventDefault()
        zone.classList.remove("active")

        const itemId = e.dataTransfer.getData("text/plain")
        const item = document.querySelector(`[data-id="${itemId}"]`)

        // Move item to drop zone
        zone.appendChild(item)

        // Call onDrop callback
        if (this.onDrop) {
          this.onDrop(item, zone)
        }
      })
    })
  }
}
