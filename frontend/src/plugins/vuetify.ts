import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import ru from 'vuetify/src/locale/ru';

Vue.use(Vuetify);

export default new Vuetify({
  lang: {
    locales: { ru },
    current: 'ru',
  },
  theme: {
    themes: {
      light: {
        primary: '#0178E6',
        secondary: '#183149',
        secondaryLight: '#8191A1',
        secondaryLightest: '#F0F4F9',
        lightest: '#fff',
        lighter: '#f5f5f5',
        light: '#eee',
        midLight: '#e4e4e4',
        midDark: '#BBBBBB',
        error: '#D53760',
        errorLight: '#F5E4EA',
        warning: '#EBCB71',
        warningLight: '#FEF9ED',
        success: '#75BC41',
        successLight: '#E9F7E9',
      },
    },
  },
});
