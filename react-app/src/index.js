import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import './index.css';
import App from './App';
import configureStore from './store';
import BrowsingHistoryProvider from './context/BrowsingHistoryContext';

const store = configureStore();

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowsingHistoryProvider>
        <App />
      </BrowsingHistoryProvider>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);
