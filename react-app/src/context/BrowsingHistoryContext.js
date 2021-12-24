import { createContext, useCallback, useContext, useState } from 'react';

export const BrowsingHistoryContext = createContext();

export const useBrowsingHistory = () => useContext(BrowsingHistoryContext);

export default function BrowsingHistoryProvider({ children }) {
    const [locations, setLocations] = useState({ visited: [window.location.pathname], currentLocation: 0 });

    const nextLocation = useCallback(
        (path) => {
            const updateVisited = locations.visited.slice(0, locations.currentLocation + 1);
            updateVisited.push(path);
            setLocations({
                visited: updateVisited,
                currentLocation: locations.currentLocation + 1
            })
        }
    )

    const goBack = useCallback(
        async () => {
            setLocations({
                visited: locations.visited,
                currentLocation: locations.currentLocation - 1
            })
        }
    );

    const goForward = useCallback(
        async () => {
            setLocations({
                visited: locations.visited,
                currentLocation: locations.currentLocation + 1
            })
        }
    );
    return (
        <BrowsingHistoryContext.Provider
            value={{ locations, setLocations, nextLocation, goBack, goForward }}>
                {children}
        </BrowsingHistoryContext.Provider>
    );
}
