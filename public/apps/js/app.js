document.addEventListener("DOMContentLoaded", function () {

    Array.prototype.same = function(array) {
        if (!array) return false;
        if (this.length !== array.length) return false;
        return this.sort().every(function(value, index) {
            return value === array.sort()[index];
        });
    };


    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form, validator) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.validator = new validator();

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {

            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    if (!this.validator.validate(this.currentStep)) return false;
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    if (!this.validator.validate(this.currentStep, false)) return false;
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {

            if (this.currentStep === 3 && this.validator.categoriesChanged()) {
                let ci = new CreateInstitutions();
                ci.renderInstitutions(this.validator.last_institution);
            }

            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            return true;
            // e.preventDefault();
            // this.currentStep++;
            // this.updateForm();
        }
    }


    class FormValidator {
        messages = {
            1: 'Aby przejść do następnego kroku musisz wybrać przynajmniej jedną kategorię.',
            2: 'Liczba worków musi być dodatnia.',
            3: 'Aby przejść do innej sekcji formularza musisz wybrać organizację.',
            4: 'Wypełnij wszystkie pola formularza (Uwagi niewymagane).',
            5: 'Problemy z walidacją formularza...',
        };

        constructor() {
            this.form = document.querySelector('div.form--steps-container form');
            this.last_categories = [];
            this.last_institution = 0;
        }

        validate(step, forward = true) {
            let valid = true;
            switch (step) {
                case 1:
                    if (forward && !this.categoryChecked()) valid = false;
                    break;
                case 2:
                    if (forward && !this.quantityPositive()) valid = false;
                    break;
                case 3:
                    if (forward && !this.institutionChecked()) valid = false;
                    this.saveLastInstitution();
                    break;
                case 4:
                    if (forward && !this.addressAndDate()) valid = false;
                    this.setSummary();
                    break;
                case 5:
                    if (forward && !this.allFormSection()) valid = false;
                    break;
            }
            if (!valid) alert(this.messages[step]);
            return valid;
        }

        getCategories() {
            let categories = [];
            this.form.querySelectorAll('input[name="categories"]:checked').forEach(function (el) {
                categories.push(parseInt(el.value));
            });
            categories.sort(function(a, b){return a-b});
            return categories;
        }

        saveLastCategories() {
            this.last_categories = this.getCategories();
        }

        categoriesChanged() {
            if (this.last_categories.same(this.getCategories())) {
                return false;
            } else {
                this.saveLastCategories();
                return true;
            }
        }

        categoryChecked() {
            let categories = this.getCategories();
            return categories.length > 0;
        }

        getQuantity() {
            return this.form.querySelector('input[name="quantity"]').value;
        }

        quantityPositive() {
            let quantity = parseInt(this.getQuantity());
            return Number.isInteger(quantity) && quantity > 0;
        }

        getInstitution() {
            let institution = this.form.querySelector('input[name="institution"]:checked');
            if (institution && Number.isInteger(parseInt(institution.value)) && institution.value > 0) {
                return parseInt(institution.value);
            } else {
                return 0;
            }
        }

        getCategoriesName() {
            let categories = [];
            this.form.querySelectorAll('input[name="categories"]:checked').forEach(function (el) {
                categories.push(el.parentElement.querySelector('.description').innerText);
            });
            return categories.join(' / ');
        }

        getInstitutionName() {
            return this.form.querySelector('input[name="institution"]:checked').parentElement.querySelector('div[class="title"]').innerHTML;
        }

        saveLastInstitution() {
            this.last_institution = this.getInstitution();
        }

        institutionChecked() {
            return this.getInstitution() > 0;
        }

        getFieldVal(fieldName) {
            return this.form.querySelector('[name="'+fieldName+'"]').value;
        }

        addressOk() {
            return this.getFieldVal('address').length > 4;
        }

        cityOk() {
            return this.getFieldVal('city').length > 2;
        }

        zipOk() {
            return this.getFieldVal('zip_code').length > 4;
        }

        phoneNumberOk() {
            return this.getFieldVal('phone_number').length > 8;
        }

        dateOk() {
            return this.getFieldVal('pick_up_date').length > 6;
        }

        timeOk() {
            return this.getFieldVal('pick_up_time').length > 3;
        }

        setSummaryField(name, value = undefined) {
            if (value === undefined) value = this.getFieldVal(name);
            this.form.querySelector('#sum_'+name).innerHTML = value;
        }

        setSummary() {
            this.setSummaryField('quantity');
            this.setSummaryField('bags_cats', this.getCategoriesName());
            this.setSummaryField('institution', this.getInstitutionName());
            this.setSummaryField('address');
            this.setSummaryField('city');
            this.setSummaryField('zip_code');
            this.setSummaryField('phone_number');
            this.setSummaryField('pick_up_date');
            this.setSummaryField('pick_up_time');
            this.setSummaryField('pick_up_comment');
        }

        addressAndDate() {
            return this.addressOk() && this.cityOk() && this.zipOk() && this.phoneNumberOk() && this.dateOk() && this.timeOk();
        }

        allFormSection() {
            return this.categoryChecked() && this.quantityPositive() && this.institutionChecked() && this.addressAndDate();
        }

    }


    class CreateInstitutions {
        constructor() {
            this.institution_div_tpl = document.querySelector('#inst_tpl>div[class*="form-group--checkbox"]');
            this.institutions_box = document.querySelector('#inst_box');
            this.api_url = 'http://127.0.0.1:8003/api/institutions-in/?format=json&categories=';
            this.categories = this.getCategories();
        }

        getCategories() {
            let categories = [];
            document.querySelectorAll('input[name="categories"]').forEach(function (el) {
                if (el.checked) categories.push(el.value);
            });
            return categories;
        }

        getCategoriesAsStr() {
            return this.categories.join(',');
        }

        clearInstitutions() {
            this.institutions_box.innerHTML = '';
        }

        addInstitution(id, name, description, checked) {
            let institution = this.institution_div_tpl.cloneNode(true);
            institution.querySelector('input').value = id;
            institution.querySelector('input').checked = (id === checked);
            institution.querySelector('div[class="title"]').innerHTML = name;
            institution.querySelector('div[class="subtitle"]').innerHTML = description;
            this.institutions_box.append(institution);
        }

        noInstitutionInfo() {
            this.institutions_box.innerHTML = document.querySelector('.no-institutions').outerHTML;
        }

        added() {
            return (this.institutions_box.innerHTML !== '')
        }

        renderInstitutions(checked) {
            this.clearInstitutions();
            let self = this;
            fetch(this.api_url + this.getCategoriesAsStr()).then((resp) => resp.json()).then(function (json) {
                for (let i of json.results) {
                    self.addInstitution(i.id, i.name, i.description, checked);
                }
                if (!self.added()) self.noInstitutionInfo();
            }).catch(function (ex) {
                alert('parsing failed' + ex);
            });
        }

    }


    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form, FormValidator);
    }


});
