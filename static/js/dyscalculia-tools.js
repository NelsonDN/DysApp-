/**
 * Dyscalculia Tools - JavaScript utilities for dyscalculia exercises
 */

// Number visualization
class NumberVisualizer {
  constructor(container) {
    this.container = container
    this.value = 0
    this.maxValue = 100
    this.itemSize = 30
    this.itemGap = 5
    this.itemsPerRow = 10
    this.itemColor = "#4E54C8"
  }

  // Set the value to visualize
  setValue(value) {
    this.value = Math.min(Math.max(0, value), this.maxValue)
    this.render()
  }

  // Render the visualization
  render() {
    // Clear container
    this.container.innerHTML = ""

    // Create visual counter
    const visualCounter = document.createElement("div")
    visualCounter.className = "visual-counter"

    // Add counter items
    for (let i = 0; i < this.value; i++) {
      const item = document.createElement("div")
      item.className = "counter-item"
      item.style.backgroundColor = this.itemColor
      item.style.width = `${this.itemSize}px`
      item.style.height = `${this.itemSize}px`

      visualCounter.appendChild(item)
    }

    this.container.appendChild(visualCounter)
  }

  // Animate counting up to a value
  animateCount(targetValue, duration = 1000) {
    const startValue = this.value
    const valueChange = targetValue - startValue
    const startTime = performance.now()

    const animate = (currentTime) => {
      const elapsedTime = currentTime - startTime
      const progress = Math.min(elapsedTime / duration, 1)

      // Calculate current value using easing function
      const easedProgress = this.easeInOutQuad(progress)
      const currentValue = Math.round(startValue + valueChange * easedProgress)

      this.setValue(currentValue)

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }

  // Easing function for smooth animation
  easeInOutQuad(t) {
    return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2
  }
}

// Number line
class NumberLine {
  constructor(container, min, max) {
    this.container = container
    this.min = min
    this.max = max
    this.value = min
    this.pointerElement = null
    this.valueDisplay = null
    this.onChange = null
  }

  // Initialize the number line
  init() {
    // Clear container
    this.container.innerHTML = ""

    // Create number line elements
    const track = document.createElement("div")
    track.className = "number-line-track"

    const markers = document.createElement("div")
    markers.className = "number-line-markers"

    const labels = document.createElement("div")
    labels.className = "number-line-labels"

    const pointer = document.createElement("div")
    pointer.className = "number-line-pointer"
    pointer.style.left = "0%"
    this.pointerElement = pointer

    // Create markers and labels
    const range = this.max - this.min
    const steps = 10

    for (let i = 0; i <= steps; i++) {
      const percent = (i / steps) * 100
      const value = this.min + range * (i / steps)

      // Create marker
      const marker = document.createElement("div")
      marker.className = "number-line-marker"
      marker.style.left = `${percent}%`
      markers.appendChild(marker)

      // Create label
      const label = document.createElement("div")
      label.className = "number-line-label"
      label.textContent = value
      label.style.left = `${percent}%`
      labels.appendChild(label)
    }

    // Add elements to track
    track.appendChild(markers)
    track.appendChild(pointer)
    track.appendChild(labels)

    // Add track to container
    this.container.appendChild(track)

    // Create value display
    const valueDisplay = document.createElement("div")
    valueDisplay.className = "text-center mt-2"
    valueDisplay.textContent = this.value
    this.valueDisplay = valueDisplay

    this.container.appendChild(valueDisplay)

    // Make number line interactive
    this.container.addEventListener("click", this.handleClick.bind(this))

    // Make pointer draggable
    this.initDraggable()
  }

  // Handle click on number line
  handleClick(e) {
    const rect = this.container.getBoundingClientRect()
    const trackRect = this.container.querySelector(".number-line-track").getBoundingClientRect()
    const x = e.clientX - trackRect.left
    const percent = (x / trackRect.width) * 100

    this.updatePointer(percent)
  }

  // Initialize draggable pointer
  initDraggable() {
    let isDragging = false

    this.pointerElement.addEventListener("mousedown", () => {
      isDragging = true
    })

    document.addEventListener("mousemove", (e) => {
      if (isDragging) {
        const trackRect = this.container.querySelector(".number-line-track").getBoundingClientRect()
        let x = e.clientX - trackRect.left

        // Constrain to track
        if (x < 0) x = 0
        if (x > trackRect.width) x = trackRect.width

        const percent = (x / trackRect.width) * 100

        this.updatePointer(percent)
      }
    })

    document.addEventListener("mouseup", () => {
      isDragging = false
    })
  }

  // Update pointer position and value
  updatePointer(percent) {
    // Constrain percent
    percent = Math.min(Math.max(0, percent), 100)

    // Update pointer position
    this.pointerElement.style.left = `${percent}%`

    // Calculate value
    const range = this.max - this.min
    this.value = Math.round(this.min + range * (percent / 100))

    // Update value display
    this.valueDisplay.textContent = this.value

    // Call onChange callback
    if (this.onChange) {
      this.onChange(this.value)
    }
  }

  // Set value programmatically
  setValue(value) {
    // Constrain value
    value = Math.min(Math.max(this.min, value), this.max)

    // Calculate percent
    const range = this.max - this.min
    const percent = ((value - this.min) / range) * 100

    this.updatePointer(percent)
  }
}

// Abacus
class Abacus {
  constructor(container) {
    this.container = container
    this.rows = []
    this.value = 0
    this.onChange = null
  }

  // Initialize the abacus
  init() {
    // Get all rows
    this.rows = Array.from(this.container.querySelectorAll(".abacus-row"))

    // Add event listeners to beads
    const beads = this.container.querySelectorAll(".abacus-bead")

    beads.forEach((bead) => {
      bead.addEventListener("click", () => {
        bead.classList.toggle("active")
        this.updateValue()
      })
    })

    // Add reset button
    const resetButton = this.container.querySelector("#reset-abacus")

    if (resetButton) {
      resetButton.addEventListener("click", () => {
        this.reset()
      })
    }
  }

  // Update the total value
  updateValue() {
    let total = 0

    const activeBeads = this.container.querySelectorAll(".abacus-bead.active")

    activeBeads.forEach((bead) => {
      total += Number.parseInt(bead.getAttribute("data-value"))
    })

    this.value = total

    // Call onChange callback
    if (this.onChange) {
      this.onChange(this.value)
    }
  }

  // Reset the abacus
  reset() {
    const beads = this.container.querySelectorAll(".abacus-bead")

    beads.forEach((bead) => {
      bead.classList.remove("active")
    })

    this.value = 0

    // Call onChange callback
    if (this.onChange) {
      this.onChange(this.value)
    }
  }

  // Set value programmatically
  setValue(value) {
    // Reset first
    this.reset()

    // Parse value
    let remainingValue = value

    // Activate beads to represent the value
    this.rows.forEach((row) => {
      const beads = Array.from(row.querySelectorAll(".abacus-bead"))
      const beadValue = Number.parseInt(beads[0].getAttribute("data-value"))

      // Calculate how many beads to activate
      const beadsToActivate = Math.min(Math.floor(remainingValue / beadValue), beads.length)

      // Activate beads
      for (let i = 0; i < beadsToActivate; i++) {
        beads[i].classList.add("active")
      }

      // Update remaining value
      remainingValue -= beadValue * beadsToActivate
    })

    this.value = value

    // Call onChange callback
    if (this.onChange) {
      this.onChange(this.value)
    }
  }
}

// Step-by-step calculation
class StepCalculator {
  constructor(container) {
    this.container = container
    this.steps = []
    this.currentStep = 0
  }

  // Set calculation steps
  setSteps(steps) {
    this.steps = steps
    this.currentStep = 0
    this.render()
  }

  // Render the calculation steps
  render() {
    // Clear container
    this.container.innerHTML = ""

    // Add steps
    this.steps.forEach((step, index) => {
      const stepElement = document.createElement("div")
      stepElement.className = "calculation-step"
      stepElement.innerHTML = step

      if (index === this.currentStep) {
        stepElement.classList.add("active")
      }

      this.container.appendChild(stepElement)
    })
  }

  // Go to next step
  nextStep() {
    if (this.currentStep < this.steps.length - 1) {
      this.currentStep++
      this.render()
      return true
    }
    return false
  }

  // Go to previous step
  prevStep() {
    if (this.currentStep > 0) {
      this.currentStep--
      this.render()
      return true
    }
    return false
  }

  // Go to specific step
  goToStep(step) {
    if (step >= 0 && step < this.steps.length) {
      this.currentStep = step
      this.render()
      return true
    }
    return false
  }
}
