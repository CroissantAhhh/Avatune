import { useHistory } from 'react-router-dom';


// A general container element for a variety of resources
// Category can be one of: Medium, Artist, Album, Playlist, User
export default function GeneralListing({ item, category }) {
    const history = useHistory();

    function redirect() {
        history.push(`/${category.toLowerCase()}/${item.hashedId}`)
    };

    return (
        <div className="general-listing" onClick={redirect}>
            <img src={item.image} alt="item image/artwork" height="200px" width="200px"></img>
            <p>{item.title}</p>
            <p>{category}</p>
        </div>
    )
}
