import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch, useLocation } from 'react-router-dom';
import { useDispatch } from 'react-redux';

import { loadUserPlaylists } from './store/playlists';

import { useBrowsingHistory } from './context/BrowsingHistoryContext';

import ScrollToTop from './utils/scrollToTop';

import LoginForm from './components/auth/LoginForm';
import SignUpForm from './components/auth/SignUpForm';
import ProtectedRoute from './components/auth/ProtectedRoute';

import PageContainer from './pages/PageContainer';
import HomePage from './pages/HomePage';
import AlbumPage from './pages/AlbumPage';
import ArtistPage from './pages/ArtistPage';
import FollowersPage from './pages/FollowersPage';
import FollowingPage from './pages/FollowingPage';
import MediumPage from './pages/MediumPage';
import PlaylistPage from './pages/PlaylistPage';
import SearchResultsPage from './pages/SearchResultsPage';
import SpecificResultsPage from './pages/SpecificResultsPage';
import SplashPage from './pages/SplashPage';
import UserPage from './pages/UserPage';
import MyCategoryPage from './pages/MyCategoryPage';
import NotFoundPage from './pages/NotFoundPage';

import { authenticate } from './store/session';

function App() {
  const [loaded, setLoaded] = useState(false);
  const dispatch = useDispatch();
  const { setLocations } = useBrowsingHistory();

  useEffect(() => {
    (async() => {
      const userId = await dispatch(authenticate());
      await dispatch(loadUserPlaylists(userId));
      setLoaded(true);
    })();
  }, [dispatch]);

  if (!loaded) {
    return null;
  }

  return (
    <BrowserRouter>
      <div className="window">
        <Switch>
          <Route path='/' exact={true}>
            <SplashPage />
          </Route>
          <Route path='/login'>
            <LoginForm />
          </Route>
          <ProtectedRoute path='/home'>
            <PageContainer page={<HomePage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/user/:userHash' exact={true}>
            <PageContainer page={<UserPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/user/:userHash/followers'>
            <PageContainer page={<FollowersPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/user/:userHash/following'>
            <PageContainer page={<FollowingPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/medium/:mediumHash'>
            <PageContainer page={<MediumPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/artist/:artistHash'>
            <PageContainer page={<ArtistPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/album/:albumHash'>
            <PageContainer page={<AlbumPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/playlist/:playlistHash'>
            <PageContainer page={<PlaylistPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/search/:searchQuery' exact={true}>
            <PageContainer page={<SearchResultsPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/search/:searchQuery/:category'>
            <PageContainer page={<SpecificResultsPage />} />
          </ProtectedRoute>
          <ProtectedRoute path='/my/:category'>
            <PageContainer page={<MyCategoryPage />} />
          </ProtectedRoute>
          <Route>
            <NotFoundPage />
          </Route>
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
