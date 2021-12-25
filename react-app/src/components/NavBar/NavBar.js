import { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { NavLink, useHistory, useLocation } from 'react-router-dom';
import Dropdown from 'react-bootstrap/Dropdown'
import { useBrowsingHistory } from '../../context/BrowsingHistoryContext';

import './NavBar.css';

export default function NavBar() {
  const history = useHistory();
  const location = useLocation();
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [title, setTitle] = useState("");
  const sessionUser = useSelector(state => state.session.user);
  const { locations, goBack, goForward, nextLocation } = useBrowsingHistory();

  function nextPath(path) {
    nextLocation(path);
    history.push(path);
  }
  useEffect(() => {
    (async() => {
      const title = await parseLocation();
      setTitle(title);
      document.title = title;
    })();
  }, [location.pathname])

  async function executeBack() {
    if (locations.currentLocation > 0) {
      await goBack();
      await history.push(locations.visited[locations.currentLocation - 1]);
    }
  }

  async function executeForward() {
    if (locations.currentLocation < locations.visited.length - 1) {
      await goForward();
      await history.push(locations.visited[locations.currentLocation + 1]);
    }
  }

  const stylePrev = {
    cursor: (locations.currentLocation > 0) ? "pointer" : "not-allowed",
    opacity: (locations.currentLocation > 0) ? 1 : 0.5,
  }

  const styleNext = {
    cursor: (locations.currentLocation < locations.visited.length - 1) ? "pointer" : "not-allowed",
    opacity: (locations.currentLocation < locations.visited.length - 1) ? 1 : 0.5,
  }

  async function parseLocation() {
    const singlePageTypes = ['user', 'medium', 'artist', 'album', 'playlist']
    const currentPath = location.pathname;
    const pathSections = currentPath.split("/").filter(str => str.length > 0);
    if (singlePageTypes.includes(pathSections[0]) && pathSections.length === 2) {
      const response = await fetch(`/api/general/${pathSections[0]}/${pathSections[1]}`)
      const title = await response.json();
      return title.title;
    }
    if (pathSections[0] === 'home') {
      return "Home";
    }
    return "";
  }

  return (
    <div className="site-nav-bar l-horizontal">
      <div className="history-controls">
        <div className="history-button rounded" onClick={executeBack} style={stylePrev}>
          <svg xmlns="http://www.w3.org/2000/svg" height="25px" width="25px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </div>
        <div className="history-button rounded" onClick={executeForward} style={styleNext}>
          <svg xmlns="http://www.w3.org/2000/svg" height="25px" width="25px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
      <div className="page-title-section">
        <p className="page-title">{title}</p>
      </div>
      <div className="profile-section l-horizontal">
        <Dropdown id="profile-dropdown" title="Profile" onClick={() => nextPath(`/user/${sessionUser.hashedId}`)}>
          <Dropdown.Toggle id="profile-button" variant="success">
            <div className="profile-button-container l-horizontal">
              <img className="profile-button-image rounded" src={sessionUser.image} height="40px" alt="profile pic" />
              <p className="profile-button-text">{sessionUser.username}</p>
              <svg xmlns="http://www.w3.org/2000/svg" height="30px" width="30px" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </div>
          </Dropdown.Toggle>
        </Dropdown>
      </div>
    </div>
  );
}
