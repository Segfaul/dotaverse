import PageForbidden from '../error/PageForbidden';
import { isAuthenticated } from '../context/AuthContext';


export type ProtectedRouteProps = {
    outlet: JSX.Element;
};
  
export default function ProtectedRoute({ outlet }: ProtectedRouteProps) {
    if(isAuthenticated()) {
        return outlet;
    } else {
        return <PageForbidden />;
    }
}