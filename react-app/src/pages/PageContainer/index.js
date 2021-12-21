import CurrentSongsProvider from "../../context/CurrentSongsContext";
import NavBar from "../../components/NavBar/NavBar";
import MusicPlayer from "../../components/MusicPlayer";

export default function PageContainer({ page }) {

    return (
        <CurrentSongsProvider>
            <div className="main-page-content">
                <NavBar />
                {page}
                <MusicPlayer />
            </div>
        </CurrentSongsProvider>
    )
}
