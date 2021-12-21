import { createContext, useCallback, useContext, useState } from 'react';

export const CurrentSongsContext = createContext();

export const useCurrentSongs = () => useContext(CurrentSongsContext);

export default function CurrentSongsProvider({ children }) {
    const [currentSongs, setCurrentSongs] = useState({ songList: [], playOrder: [], currentPosition: 0, isShuffle: false});

    function shuffle(array) {
        let currentIndex = array.length, randomIndex;

        // While there remain elements to shuffle...
        while (currentIndex !== 0) {

          // Pick a remaining element...
          randomIndex = Math.floor(Math.random() * currentIndex);
          currentIndex--;

          // And swap it with the current element.
          [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
        }
        return array;
    }
    //                         currentPosition=10
    // order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    // SHUFFLE
    //     currentPosition = 0
    // order = [9, 12, 2, 1, 5, 14, 19, 3, 4, 6, 16, 18, 7, 8, .....]
    const injectSongs = useCallback(
        (tracks, position, isShuffle) => {
            if (isShuffle) {
                const startingPosition = position
                const remainingSongs = tracks.map((element, index) => index).filter(index => index !== startingPosition);
                const shuffledOrder = [startingPosition, ...shuffle(remainingSongs)];
                setCurrentSongs({
                    songList: tracks,
                    playOrder: shuffledOrder,
                    currentPosition: 0,
                    isShuffle
                });
            } else {
                const normalOrder = tracks.map((element, index) => index);
                let currentSongPosition;
                if (currentSongs?.playOrder.length) {
                    currentSongPosition = currentSongs?.playOrder[position]
                } else {
                    currentSongPosition = position;
                }

                setCurrentSongs({
                    songList: tracks,
                    playOrder: normalOrder,
                    currentPosition: currentSongPosition,
                    isShuffle
                });
            }
        },
        [currentSongs, setCurrentSongs]
    );

    return (
        <CurrentSongsContext.Provider
            value={{currentSongs, setCurrentSongs, injectSongs}}>
                {children}
        </CurrentSongsContext.Provider>
    );
}
