// Vue.createApp({
//     name: "App",
//     components: {
//         VForm: VeeValidate.Form,
//         VField: VeeValidate.Field,
//         ErrorMessage: VeeValidate.ErrorMessage,
//     },
//     data() {
//         return {
//             schema1: {
//                 lvls: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' количество уровней';
//                 },
//                 form: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' форму торта';
//                 },
//                 topping: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' топпинг';
//                 }
//             },
//             schema2: {
//                 name: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' имя';
//                 },
//                 phone: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' телефон';
//                 },
//                 name_format: (value) => {
//                     const regex = /^[a-zA-Zа-яА-Я]+$/
//                     if (!value) {
//                         return true;
//                     }
//                     if ( !regex.test(value)) {

//                         return '⚠ Формат имени нарушен';
//                     }
//                     return true;
//                 },
//                 email_format: (value) => {
//                     const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
//                     if (!value) {
//                         return true;
//                     }
//                     if ( !regex.test(value)) {

//                         return '⚠ Формат почты нарушен';
//                     }
//                     return true;
//                 },
//                 phone_format:(value) => {
//                     const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
//                     if (!value) {
//                         return true;
//                     }
//                     if ( !regex.test(value)) {

//                         return '⚠ Формат телефона нарушен';
//                     }
//                     return true;
//                 },
//                 email: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' почту';
//                 },
//                 address: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' адрес';
//                 },
//                 date: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' дату доставки';
//                 },
//                 time: (value) => {
//                     if (value) {
//                         return true;
//                     }
//                     return ' время доставки';
//                 }
//             },
//             DATA: {
//                 Levels: ['не выбрано', '1', '2', '3'],
//                 Forms: ['не выбрано', 'Круг', 'Квадрат', 'Прямоугольник'],
//                 Toppings: ['не выбрано', 'Без', 'Белый соус', 'Карамельный', 'Кленовый', 'Черничный', 'Молочный шоколад', 'Клубничный'],
//                 Berries: ['нет', 'Ежевика', 'Малина', 'Голубика', 'Клубника'],
//                 Decors: [ 'нет', 'Фисташки', 'Безе', 'Фундук', 'Пекан', 'Маршмеллоу', 'Марципан']
//             },
//             Costs: {
//                 Levels: [0, 400, 750, 1100],
//                 Forms: [0, 600, 400, 1000],
//                 Toppings: [0, 0, 200, 180, 200, 300, 350, 200],
//                 Berries: [0, 400, 300, 450, 500],
//                 Decors: [0, 300, 400, 350, 300, 200, 280],
//                 Words: 500
//             },
//             Levels: 0,
//             Form: 0,
//             Topping: 0,
//             Berries: 0,
//             Decor: 0,
//             Words: '',
//             Comments: '',
//             Designed: false,

//             Name: '',
//             Phone: null,
//             Email: null,
//             Address: null,
//             Dates: null,
//             Time: null,
//             DelivComments: ''
//         }
//     },
//     methods: {
//         ToStep4() {
//             this.Designed = true
//             setTimeout(() => this.$refs.ToStep4.click(), 0);
//         }
//     },
//     computed: {
//         Cost() {
//             let W = this.Words ? this.Costs.Words : 0
//             return this.Costs.Levels[this.Levels] + this.Costs.Forms[this.Form] +
//                 this.Costs.Toppings[this.Topping] + this.Costs.Berries[this.Berries] +
//                 this.Costs.Decors[this.Decor] + W
//         }
//     }
// }).mount('#VueApp')




// !!!!!!!!!!!!!!!!!!
// static/js/index.js  — ПОЛНАЯ ЗАМЕНА
// (function () {
//   const { createApp } = Vue;

//   function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== "") {
//       const cookies = document.cookie.split(";");
//       for (let i = 0; i < cookies.length; i++) {
//         const cookie = cookies[i].trim();
//         if (cookie.substring(0, name.length + 1) === (name + "=")) {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//         }
//       }
//     }
//     return cookieValue;
//   }

//   createApp({
//     components: {
//       "v-form": VeeValidate.Form,
//       "v-field": VeeValidate.Field,
//       "error-message": VeeValidate.ErrorMessage,
//     },

//     data() {
//       return {
//         // выбор торта
//         Levels: "",   // обязателен
//         Form: "",     // обязателен
//         Topping: "",  // обязателен
//         Berries: "",  // опционально (single-choice как сейчас)
//         Decor: "",    // опционально (single-choice как сейчас)
//         Words: "",
//         Comments: "",

//         // шаг оформления
//         Designed: false,

//         // доставка/контакты
//         Name: "",
//         Phone: "",
//         Email: "",
//         Address: "",
//         Dates: "",
//         Time: "",
//         DelivComments: "",

//         // цена в правом верхнем углу
//         Cost: 0,

//         // чтобы vee-validate не ругался на :validation-schema
//         schema1: {},
//         schema2: {},
//       };
//     },

//     mounted() {
//       // при первом рендере тоже попробуем посчитать (вернётся 0, если не выбраны обязательные)
//       this.updateCost();
//     },

//     watch: {
//       Levels: "updateCost",
//       Form: "updateCost",
//       Topping: "updateCost",
//       Berries: "updateCost",
//       Decor: "updateCost",
//       Words: "updateCost",
//     },

//     methods: {
//       ToStep4() {
//         this.Designed = true;
//         // прокрутка к оформлению
//         try { location.hash = "#step4"; } catch (_) {}
//       },

//       async updateCost() {
//         try {
//           const fd = new FormData();
//           if (this.Levels)  fd.append("LEVELS", this.Levels);
//           if (this.Form)    fd.append("FORM", this.Form);
//           if (this.Topping) fd.append("TOPPING", this.Topping);
//           if (this.Berries) fd.append("BERRIES", this.Berries);
//           if (this.Decor)   fd.append("DECOR", this.Decor);
//           if ((this.Words || "").trim()) fd.append("WORDS", this.Words);

//           const resp = await fetch("/orders/price/", {
//             method: "POST",
//             headers: { "X-CSRFToken": getCookie("csrftoken") },
//             body: fd,
//           });

//           if (!resp.ok) {
//             this.Cost = 0;
//             return;
//           }

//           const data = await resp.json();
//           const p = Number(data && data.price);
//           this.Cost = Number.isFinite(p) ? p : 0; // никаких NaN
//         } catch (e) {
//           this.Cost = 0;
//         }
//       },
//     },
//   }).mount("#VueApp");
// })();




/* ===== CakeBake front (Vue 3) ===== */
document.addEventListener('DOMContentLoaded', () => {
  const mountEl = document.getElementById('VueApp');
  if (!mountEl) return console.warn('[CakeBake] #VueApp not found');

  if (!window.Vue) {
    console.error('[CakeBake] Vue is not loaded.');
    return;
  }

  console.log('[CakeBake] boot…');

  const { createApp, ref, watch, onMounted } = Vue;

  // vee-validate может не подтянуться из CDN — дадим «заглушки», чтобы шаблон не падал
  const V = window.VeeValidate || {};
  const FormComp = V.Form || {
    emits: ['submit'],
    template: `<form @submit.prevent="$emit('submit')"><slot/></form>`,
  };
  const FieldComp = V.Field || {
    inheritAttrs: false,
    props: ['modelValue', 'type', 'name', 'value', 'id'],
    emits: ['update:modelValue'],
    computed: {
      isChecked() {
        return this.type === 'radio'
          ? String(this.modelValue) === String(this.value)
          : this.modelValue;
      },
    },
    methods: {
      onChange(e) {
        const val = this.type === 'radio' ? this.value : e.target.value;
        this.$emit('update:modelValue', val);
      },
    },
    template: `
      <input
        v-bind="$attrs"
        :id="id"
        :type="type || 'text'"
        :name="name"
        :value="value"
        :checked="isChecked"
        @input="onChange"
        @change="onChange"
      />
    `,
  };
  const ErrorComp = V.ErrorMessage || { template: `<span></span>` };

  function getCookie(name) {
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : '';
  }

  const app = createApp({
    setup() {
      // выборы конструктора
      const Levels   = ref(null);
      const FormSel  = ref(null); // нельзя называть "Form" — конфликтует с компонентом
      const Topping  = ref(null);
      const Berries  = ref(null);
      const Decor    = ref(null);
      const Words    = ref('');
      const Comments = ref('');

      // шаг оформления
      const Name          = ref('');
      const Phone         = ref('');
      const Email         = ref('');
      const Address       = ref('');
      const Dates         = ref('');
      const Time          = ref('');
      const DelivComments = ref('');

      // UI
      const Designed = ref(false);
      const Cost     = ref(0);

      // словари для карточки справа
      const DATA = ref(window.DATA || {
        Levels: {}, Forms: {}, Toppings: {}, Berries: {}, Decors: {}
      });

      async function recalcPrice() {
        // ничего не выбрано — ноль и выходим
        const any =
          Levels.value || FormSel.value || Topping.value ||
          Berries.value || Decor.value || (Words.value && Words.value.trim());
        if (!any) { Cost.value = 0; return; }

        const p = new URLSearchParams();
        if (Levels.value)  p.append('LEVELS',  Levels.value);
        if (FormSel.value) p.append('FORM',    FormSel.value);
        if (Topping.value) p.append('TOPPING', Topping.value);
        if (Berries.value) p.append('BERRIES', Berries.value);
        if (Decor.value)   p.append('DECOR',   Decor.value);
        if (Words.value && Words.value.trim()) p.append('WORDS', Words.value.trim());

        try {
          const res = await fetch('/orders/price/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
              'X-CSRFToken': getCookie('csrftoken'),
              'X-Requested-With': 'XMLHttpRequest',
            },
            body: p.toString(),
          });
          const data = await res.json();
          if (typeof data.price === 'number' && isFinite(data.price)) {
            Cost.value = Math.round(data.price);
          }
        } catch (e) {
          console.error('[CakeBake] price error', e);
        }
      }

      function ToStep4() {
        // по ТЗ обязательны 3 селекта
        if (!Levels.value || !FormSel.value || !Topping.value) {
          alert('Пожалуйста, выберите количество уровней, форму и топпинг.');
          return;
        }
        Designed.value = true;
        // прокрутка/якорь
        try { location.hash = '#step4'; } catch (_) {}
        recalcPrice();
      }

      // пересчет цены на любые изменения
      watch([Levels, FormSel, Topping, Berries, Decor, Words], recalcPrice);

      onMounted(() => {
        // первый пересчет
        recalcPrice();
        console.log('[CakeBake] mounted');
      });

      return {
        // модели
        Levels, Form: FormSel, Topping, Berries, Decor, Words, Comments,
        Name, Phone, Email, Address, Dates, Time, DelivComments,
        Designed, Cost, DATA,
        // действия
        ToStep4,
      };
    },
  });

  // регистрация компонентов (vee-validate или заглушки)
  app.component('v-form', FormComp);
  app.component('v-field', FieldComp);
  app.component('error-message', ErrorComp);

  // один mount
  app.mount('#VueApp');
});
