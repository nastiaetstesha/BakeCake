document.addEventListener('DOMContentLoaded', () => {
  const mountEl = document.getElementById('VueApp');
  if (!mountEl) return console.warn('[CakeBake] #VueApp not found');

  if (!window.Vue) {
    console.error('[CakeBake] Vue is not loaded.');
    return;
  }

  console.log('[CakeBake] boot…');

  const { createApp, ref, watch, onMounted } = Vue;

  // vee-validate может не подтянуться из CDN — дадим «заглушки»
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
      // --- выбранный базовый торт (с бэка) ---
      const selectedCake = ref(window.initialSelectedCake || null);
      const baseCakeId   = ref(selectedCake.value ? selectedCake.value.id : null);


      // выборы конструктора
      const Levels   = ref(null);
      const FormSel  = ref(null);
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
        // если выбран готовый торт → цена от него + надбавки за кастом
        let basePrice = 0;
        if (selectedCake.value && typeof selectedCake.value.price === 'number') {
          basePrice = selectedCake.value.price;
        }

        const any =
          Levels.value || FormSel.value || Topping.value ||
          Berries.value || Decor.value || (Words.value && Words.value.trim());

        if (!any && !basePrice) {
          Cost.value = 0;
          return;
        }

        async function recalcPrice() {
  const p = new URLSearchParams();
  if (baseCakeId.value) p.append('CAKE_ID', baseCakeId.value);
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
      // ВАЖНО: сервер уже вернул И базу, и допы → ничего не прибавляем
      Cost.value = Math.round(data.price);
    } else {
      Cost.value = 0;
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
        try { location.hash = '#step4'; } catch (_) {}
        recalcPrice();
      }

      // пересчет цены на любые изменения
      watch([Levels, FormSel, Topping, Berries, Decor, Words], recalcPrice);

      onMounted(() => {
  recalcPrice();              // <-- даже если опции не выбраны, подтянет базу
  console.log('[CakeBake] mounted');
});

return {
  // ...
  selectedCake, baseCakeId,   // <-- чтобы скрытый инпут получил id торта
  // ...
};


      return {
        // базовый торт
        selectedCake, baseCakeId,
        // модели конструктора
        Levels, Form: FormSel, Topping, Berries, Decor, Words, Comments,
        // данные клиента
        Name, Phone, Email, Address, Dates, Time, DelivComments,
        // UI
        Designed, Cost, DATA,
        // методы
        ToStep4,
      };
    },
  });

  // регистрация компонентов (vee-validate или заглушки)
  app.component('v-form', FormComp);
  app.component('v-field', FieldComp);
  app.component('error-message', ErrorComp);

  // mount
  app.mount('#VueApp');
});
