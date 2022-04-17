
import News from '../../../src/components/News.js'
import {mountQuasar} from '@quasar/quasar-app-extension-testing-unit-jest';


describe('Strategy Component tests: ', () => {

    test('News mount without errors', () => {
        const wrapper = mountQuasar(News);
    
        expect(wrapper).toBeTruthy();
      });
});