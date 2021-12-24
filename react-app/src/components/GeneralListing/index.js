import { useHistory } from 'react-router-dom';
import { useBrowsingHistory } from '../../context/BrowsingHistoryContext';

import "./GeneralListing.css";

// A general container element for a variety of resources
// Category can be one of: Medium, Artist, Album, Playlist, User
export default function GeneralListing({ item, category }) {
    const history = useHistory();
    const { nextLocation } = useBrowsingHistory();

    function nextPath(path) {
        nextLocation(path);
        history.push(path);
    }

    return (
        <div className="general-listing hover-pointer" onClick={() => nextPath(`/${category.toLowerCase()}/${item.hashedId}`)}>
            <img className={(category === 'User' || category ==='Artist') ? "rounded shadowed" : "shadowed" }src={item.image} alt="item image/artwork" height="200px" width="200px"></img>
            <div className="general-listing-text">
                <p className="general-listing-title">{category === 'User' ? item.username : item.title}</p>
                <p className="general-listing-category">{category}</p>
            </div>
        </div>
    )
}
