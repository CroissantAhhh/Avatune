import CurrentSongsProvider from "../../context/CurrentSongsContext";
import NavBar from "../../components/NavBar/NavBar";
import MusicPlayer from "../../components/MusicPlayer";
import SideBar from "../../components/SideBar";

import './PageContainer.css';

export default function PageContainer({ page }) {

    return (
        <CurrentSongsProvider>
            <div className="main-page l-vertical">
                <div className="main-page-upper l-horizontal">
                    <div className="main-page-left">
                        <SideBar />
                    </div>
                    <div className="main-page-middle l-vertical">
                        <div className="main-page-nav">
                            <NavBar />
                        </div>
                        <div className="main-page-content">
                            {page}
                        </div>
                    </div>
                    <div className="main-page-right">
                        UNDER CONSTRUCTION
                    </div>
                </div>
                <div className="main-page-lower">
                    <MusicPlayer />
                </div>
            </div>
        </CurrentSongsProvider>
    )
}
