import { useState, useEffect } from 'react';
import { NavLink, useHistory, useLocation } from 'react-router-dom';
import { useBrowsingHistory } from '../../context/BrowsingHistoryContext';

import './NavBar.css';

export default function NavBar() {
  const history = useHistory();
  const location = useLocation();
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [title, setTitle] = useState("");
  const { locations, goBack, goForward } = useBrowsingHistory();

  function updateWidth() {
    setWindowWidth(window.innerWidth)
  }

  useEffect(() => {
    window.addEventListener("resize", updateWidth);
    return () => window.removeEventListener("resize", updateWidth);
  });

  useEffect(() => {
    (async() => {
      console.log('triggered')
      const title = await parseLocation();
      console.log(title)
      setTitle(title);
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
        <div className="history-button" onClick={executeBack} style={stylePrev}>
          <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </div>
        <div className="history-button" onClick={executeForward} style={styleNext}>
          <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="20px" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>
      <div className="page-title-section">
        <p className="page-title">{title}</p>
      </div>
      <div className="dynamic-sections">
        <div className="search-section">

        </div>
        <div className="profile-section">

        </div>
      </div>
    </div>
  );
}
