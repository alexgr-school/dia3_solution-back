import React from 'react';
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from './ui/alert-dialog';
import { act } from 'react-dom/test-utils';

type AlertModalProps = {
    title: string;
    message: string;
    actionText?: string;
    actionFunction?: () => void;
};

const AlertModal = ({
    title,
    message,
    actionText,
    actionFunction,
}: AlertModalProps) => {
    return (
        <AlertDialog defaultOpen>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>{title}</AlertDialogTitle>
                    <AlertDialogDescription>{message}</AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Close</AlertDialogCancel>
                    <AlertDialogAction onClick={actionFunction}>
                        {actionText || 'Continue'}
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
};

export default AlertModal;
